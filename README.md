# vgw-redundancy-poller
Tool which helps you quickly determine if your VGWs have physical redundancy at the datacenter location, AWS router and/or connection layer.

## System Requirements
<ul>
 <li>python3.7</li>
 <li>boto3 - you can install with 'pip install boto3'</li>
 </ul>

## Usage Instructions
<ol>
<li>Launch the <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=ParentAccountVgwRedundancyPollerRole&templateURL=https://s3.amazonaws.com/secure-options/vgw-redundancy-poller/primary_account.json">primary_account.json</a> Cloudformation template in the AWS account that you want to run the VGW Redundancy Poller tool in. This template will create the necessary IAM permissions role for the tool to be able to describe VGWs and their associated connections</li>
 <br>
 <li>Once you have created the IAM role through the primary_account.json Cloudformation stack, you need to assume the role from  an EC2 that you intend to run the VGW Poller tool on. To do this from the AWS Management console:
   <ol> 
     <li>Go to the <strong>EC2</strong> console</li>
     <li>Right-click the EC2 that you want to assume the role</li>
     <li>Select <strong>Instance Settings</strong></li>
     <li>Select <strong>Attach/Replace IAM Role</strong></li>
     <li>From the dropdown, select <strong>ParentVgwRedundancyPollerRole</strong></li>
   </ol>
     <br>
<li>If you have any secondary AWS accounts that you want to poll with the tool, you must first deploy the <a href="https://console.aws.amazon.com/cloudformation/home?region=us-east-1#/stacks/new?stackName=SecondaryAccountVgwRedundancyPollerRole&templateURL=https://s3.amazonaws.com/secure-options/vgw-redundancy-poller/secondary_acct.json">secondary_account.json</a> template in those account(s). If you do not do this, the tool will detect "AccessDenied" against the account and skip over it</li>
 <br>
 <li>Download the tool</li>
     <code>wget https://raw.githubusercontent.com/secureoptions/vgw-redundancy-poller/master/vgw_poller.py</code><br>
 <li>Run the tool</li>
     <code>python vgw_poller.py</code>
</ol>

## Understanding the output of the tool
When running the tool, you will see output with information about every Virtual Private Gateway (VGW) under the account(s) that have a Direct Connect VIF attached to them (or attached to the Direct Connect Gateway associated with the VGW).

Here are the fields for each VGW:<br>
   <strong>Account:</strong> The AWS account number that owns the VGW<br>
   <strong>Region:</strong> The AWS region the VGW is in<br>
   <strong>Datacenter Redundancy:</strong> Whether you have physical, on-prem colo redundancy to the VGW<br>
   <strong>AWS Endpoint Redundancy:</strong> Whether the DX VIFs currently connected to the VGW reside on more than one AWS router endpoint.<br>
   <strong>Connection Redundancy:</strong> Whether the DX VIFs currently connected to the VGW reside on more than one Direct Connect link (Note: the tool does not recognize single LAGs as more than one link)<br>
<strong>Redundancy via DX Gateway(s):</strong> Whether the above mentioned layers of redundancy may be through a Direct Connect Gateway(s) that the VGW is associated with, and not necessarily directly with the VGW itself.<br>
<strong>Relevant DX Gateway Id(s):</strong> The Direct Connect Gateways that the redundancy comes through<br>
<strong>VIFs:</strong>The VIFs associated with the VGW itself and/or attached with the Direct Connect Gateway that the VGW is associated with.<br>
   
   
