# vgw-redundancy-poller
Tool which helps you quickly determine if your VGWs have physical redundancy at the datacenter location, AWS router and/or connection layer.

## Usage Instructions
<ol>
<li>Launch the primary_account.json Cloudformation template in the AWS account that you want to run the VGW Redundancy Poller tool in. This template will create the necessary IAM permissions role for the tool to be able to describe VGWs and their associated connections</li>
</ol>
