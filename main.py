import os
import subprocess

name = 'requests'
packages = ['requests']
local_files = []
python_version = 'python3.10'


layer_dir = f"{name}"
package_dir = f"{layer_dir}/python/lib/{python_version}/site-packages"

# Cleanup any previous runs
os.system(f'rm -rf {layer_dir}')


# Generate a Dockerfile
print('check here for aws registry: https://gallery.ecr.aws/lambda/python')
dockerfile_content = f"""
FROM public.ecr.aws/lambda/{python_version.replace('thon3', 'thon:3')}

WORKDIR /temp


""" 

for package in packages: 
    line = f'RUN pip install {package} -t ./'
    dockerfile_content = dockerfile_content +'\n' +line
    
    
with open('Dockerfile', 'w') as f:
    f.write(dockerfile_content)

# Build the Docker image
os.system(f"docker build -t {name} -f Dockerfile .")

# Create a temporary container to copy files from
container_id = subprocess.getoutput(f"docker create {name}")

# Copy the installed package from the container to the host machine
os.makedirs(package_dir, exist_ok=True)
os.system(f"docker cp {container_id}:./temp {package_dir}")
os.system(f'mv {package_dir}/temp/* {package_dir}')
os.system(f'rm -rf {package_dir}/temp')


# Add local files to the package directory
for local_file in local_files: 
    os.system(f'cp {local_file} {package_dir}')


# Cleanup the temporary container
os.system(f"docker rm -v {container_id}")

# Zip the package to create the Lambda layer zip
os.chdir(name)
os.system(f"zip -r {name}.zip python")
os.chdir('..')
os.system('rm Dockerfile')
#os.system('docker system prune -a -f')


print(f"{name}.zip is ready!")
print(f"docker run -it --entrypoint /bin/bash {name}")
