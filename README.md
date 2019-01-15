# vgw-redundancy-poller
Tool which helps you quickly determine if your VGWs have physical redundancy at the datacenter location, AWS router and/or connection layer.

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
</ol>

## Understanding the output of the tool
When running the tool, you will see output with information about every Virtual Private Gateway (VGW) under the account(s) that have a Direct Connect VIF attached to them (or attached to the Direct Connect Gateway associated with the VGW).

Here are the fields for each VGW:
   <strong>Account:</strong>  The AWS account number that owns the VGW
   
