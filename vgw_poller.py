import boto3
from botocore.exceptions import ClientError
from sys import argv
import re

ec2 = boto3.client('ec2')
sts = boto3.client('sts')
regions = ec2.describe_regions()

def question():
    user_answer = input("\n\nPlease provide any secondary AWS accounts (separated by commas) that\n"
                            "you want to check VGWs in. If you only want to check redundancy for\n"
                            "this account alone, hit any key to continue:\n"
                            "----------------------------------------------------------------------\n"
                            "> ") or "self"

    user_answer = user_answer.lower()
    permitted = re.match(r"( ?\d{4}\-?\d{4}\-?\d{4} ?\,?)*", user_answer)
    if permitted:
        return permitted.group(0)
    elif user_answer == 'self':
        return user_answer
    else:
        print("\nPlease provide AWS secondary account id(s) separated by commas\n"
              "or hit 'Enter' to only run the tool in this account")
        question()

def poll_vgws(account):
    vgws_dict = {}
    # Get the VGW ids in each region of this account
    vgws = dx.describe_virtual_gateways()
    for vgw in vgws['virtualGateways']:
        vgw = vgw['virtualGatewayId']
        vgws_dict[vgw] = {}
    
    # Now describe all the VIFs in this account, and append them to the relevant VGW dict
    vifs = dx.describe_virtual_interfaces()
    for vif in vifs['virtualInterfaces']:
        for vgw in vgws_dict:
            if vif['virtualGatewayId'] == vgw:
                # the VIF is associated with the VGW. Append this VIFs metadata to the VGW dict
                vgws_dict[vgw].update({vif['virtualInterfaceId'] : vif})

    for vgw in vgws_dict:
        datacenter_redundant = 'No'
        device_redundant = 'No'
        connection_redundant = 'No'
        dx_gw_associated = 'No'
        # For each VGW in dict, describe its DX GW association(s) and get the id(s)
        dxgws = dx.describe_direct_connect_gateway_associations(
        virtualGatewayId=vgw
        )
        for gw in dxgws['directConnectGatewayAssociations']:
            # describe each VIF attached to each DX GW 
            vif_attachments = dx.describe_direct_connect_gateway_attachments(
                directConnectGatewayId=gw['directConnectGatewayId']
            )
            # If there is even one VIF attached to GW, then mark GW as associated with VGW
            if vif_attachments['directConnectGatewayAttachments'] != []:
                dx_gw_associated = 'Yes'
            # record each returned VIF as being associated with the VGW
            for attach in vif_attachments['directConnectGatewayAttachments']:
                vifs = dx.describe_virtual_interfaces(
                    virtualInterfaceId=attach['virtualInterfaceId']
                )
                vgws_dict[vgw].update({attach['virtualInterfaceId'] : vifs['virtualInterfaces'][0]})
        

        if len(vgws_dict[vgw]) >= 1:
            vif_A = list(vgws_dict[vgw])[0]
            vif_dx_conn_A = vgws_dict[vgw][vif_A]['connectionId']
            vif_dx_location_A = vgws_dict[vgw][vif_A]['location']
            vif_dx_device_A = vgws_dict[vgw][vif_A]['awsDeviceV2']

            for vif_B in vgws_dict[vgw]:
                vif_dx_conn_B = vgws_dict[vgw][vif_B]['connectionId']
                vif_dx_location_B = vgws_dict[vgw][vif_B]['location']
                vif_dx_device_B = vgws_dict[vgw][vif_B]['awsDeviceV2']

                # First check to make sure they're not the same DX VIF
                if vif_B != vif_A:
                    # Check if VIF is datacenter redundant
                    if vif_dx_location_B != vif_dx_location_A:
                        datacenter_redundant = 'Yes'
                    
                    # Check if VIF is AWS endpoint redundant
                    if vif_dx_device_B != vif_dx_device_A:
                        device_redundant = 'Yes'

                    # Check if VIF is DX Conn redundant
                    if vif_dx_conn_B != vif_dx_conn_A:
                        connection_redundant = 'Yes'

            # Check if this poll is just run for the parent account
            if account == 'self':
                acct_id = sts.get_caller_identity()
                acct_id = acct_id['Account']
                account = '[Self] %s' % acct_id
                   
            print("\n\n==============================================\n"
                "Virtual Private Gateway: %s\n"
                "    Account: %s\n"
                "    Region: %s\n"
                "    Datacenter Redundancy: %s\n"
                "    AWS Endpoint Redundancy: %s\n"
                "    Connection Redundancy: %s\n"
                "    Redundant via DX Gateway(s): %s\n" 
                "    Relevant DX Gateway Id(s):" % (vgw, account, region, datacenter_redundant,device_redundant,connection_redundant,dx_gw_associated))
            if dx_gw_associated == 'Yes':
                for gw in dxgws['directConnectGatewayAssociations']:
                    print("        %s" % gw['directConnectGatewayId'])
            else:
                print("            N/A")
            print("    VIFs:")
            for vif in vgws_dict[vgw]:
                print("        %s\n"
                    "            DC: %s\n"
                    "            Endpoint: %s\n"
                    "            Conn: %s"
                    % (vif,vgws_dict[vgw][vif]['location'],vgws_dict[vgw][vif]['awsDeviceV2'],vgws_dict[vgw][vif]['connectionId']))        


user_answer = question()
print("\n\n"
    "Please wait while the tool checks your VGWs...")
this_account = sts.get_caller_identity()
this_account = this_account['Account']

if user_answer == 'self':
    # loop through each region in this account
    print("\n======== Polling Account %s ========" % this_account)
    for region in regions['Regions']:
        region = region['RegionName']
        dx = boto3.client('directconnect', region_name = region )
        poll_vgws(user_answer)
else:
    # format user inputed accounts to be usable by program
    user_answer = user_answer.replace('-','').replace(' ','')
    user_answer = user_answer.split(',')
    
    # loop through each region in this account
    print("\n======== Polling Account %s ========" % this_account)
    for region in regions['Regions']:
        region = region['RegionName']
        dx = boto3.client('directconnect', region_name = region )
        poll_vgws('self')

    # iterate through each account and assume relevant role

    for account in user_answer:
        try:
            print("\n======== Polling Account %s ========" % account)
            for region in regions['Regions']:
                region = region['RegionName']

                creds = sts.assume_role(
                    RoleArn='arn:aws:iam::' + account + ':role/VgwRedundancyPollerRole',
                    RoleSessionName='PollVgwRedundancy',
                )

                dx = boto3.client(
                'directconnect',
                region_name = region,
                aws_access_key_id=creds['Credentials']['AccessKeyId'],
                aws_secret_access_key=creds['Credentials']['SecretAccessKey'],
                aws_session_token=creds['Credentials']['SessionToken']
                )
                poll_vgws(account)

        except ClientError as e:
            if e.response['Error']['Code'] == 'AccessDenied':
                print("\n%s does not seem to accessible. Make\n"
                    "sure you have deployed the 'secondary_account'\n"
                    "Cloudformation template in any secondary accounts.\n" % account)
            pass


 