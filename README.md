# vgw-redundancy-poller
Tool which helps you quickly determine if your VGWs have physical redundancy at the datacenter location, AWS router and/or connection layer.

## Usage Instructions
<ol>
<li>Launch the primary_account.json Cloudformation template in the AWS account that you want to run the VGW Redundancy Poller tool in. This template will create the necessary IAM permissions role for the tool to be able to describe VGWs and their associated connections</li>
 <li>Once you have created the IAM role through the primary_account.json Cloudformation stack, you need to assume the role from  an EC2 that you intend to run the VGW Poller tool on. To do this from the AWS Management console:
   <ol> 
     <li>Go to the <strong>EC2</strong> console</li>
     <li>Right-click the EC2 that you want to assume the role</li>
     <li>Select <strong>Instance Settings</strong></li>
     <li>Select <strong>Attach/Replace IAM Role</strong></li>
     <li>From the dropdown, select <strong>ParentVgwPollerRole</strong></li>
   </ol>
     
<li>If you have any secondary AWS accounts that you want to poll with the tool, you must first deploy the secondary_account.json template in those account(s). If you do not do this, the tool will detect "AccessDenied" against the account and skip over it</li>
</ol>

## Understanding the output of the tool
When running the tool, you will see output with information about every Virtual Private Gateway (VGW) under the account(s) that have a Direct Connect VIF attached to them (or attached to the Direct Connect Gateway associated with the VGW).
