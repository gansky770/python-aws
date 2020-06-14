python
1.install pip (for windows :C:\**********\Python35\Scripts  >>>>>>>add to Environmental Variables and under System variables locate the Path variable, )
2.install boto

4.must install aws cli : windows( https://s3.amazonaws.com/aws-cli/AWSCLI64PY3.msi) linux (https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2-linux.html)
###curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
unzip awscliv2.zip
sudo ./aws/install###
5. put the config &cred files in ./.aws/ folder  (run aws configure >>>its creat  the folder automaticly) ## dir : linux >> ls  ~/.aws  windows: C:\> dir "%UserProfile%\.aws"

docker run -ti -v '$(pwd)':~/.aws  python:latest