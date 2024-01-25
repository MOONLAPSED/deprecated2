/.github/nfs_init.yml: This workflow will automatically configure the NFS server, mount the NFS share, and run the Docker container whenever a push is made to the repository.

Here's a breakdown of the workflow:


name: Setup NFS and Run Docker Container
This line defines the name of the workflow, which is displayed in the GitHub Actions interface.


on: [push]
This line specifies that the workflow should be triggered whenever a push is made to the repository. This means that the workflow will run automatically whenever you commit and push changes to your code.


jobs:
  setup-nfs-and-run-container:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout code
        uses: actions/checkout@v3
This section defines a job named setup-nfs-and-run-container. This job will be executed on an Ubuntu-based runner provided by GitHub Actions. The first step in the job checks out the code from your repository to the runner's working directory.


      - name: Install NFS server
        run: |
          sudo apt-get update && sudo apt-get install -y nfs-kernel-server
This step installs the NFS kernel server package using sudo apt-get install -y nfs-kernel-server. This command requires administrative privileges (sudo) and installs the NFS server software.


      - name: Create NFS share directory
        run: |
          sudo mkdir -p /shared
This step creates a directory /shared using sudo mkdir -p /shared. This directory will serve as the NFS share that clients can mount and access.


      - name: Configure NFS exports
        run: |
          echo "/shared *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports
This step defines an NFS export for the /shared directory using echo "/shared *(rw,sync,no_subtree_check,no_root_squash)" | sudo tee -a /etc/exports. This line adds an entry to the /etc/exports file, which defines the NFS exports. The *(rw,sync,no_subtree_check,no_root_squash) options allow read-write access for all clients, enable synchronous writes, disable subtree checking, and allow root users to access the share without root squashing.


      - name: Restart NFS server
        run: |
          sudo systemctl restart nfs-kernel-server
This step restarts the NFS server using sudo systemctl restart nfs-kernel-server. This ensures that the new NFS export configuration is applied.


      - name: Open NFS ports
        run: |
          sudo ufw allow 2049/tcp
          sudo ufw allow 2049/udp
This step opens the necessary NFS ports in the firewall using sudo ufw allow 2049/tcp and sudo ufw allow 2049/udp. These ports are required for NFS communication between the server and clients.


      - name: Install Docker
        run: |
          sudo apt-get update && sudo apt-get install -y docker.io
This step installs Docker using sudo apt-get update && sudo apt-get install -y docker.io. This command requires administrative privileges (sudo) and installs the Docker engine.


      - name: Start Docker container with NFS volume
        run: |
          docker run -v <server_ip>:/shared:/cntnt_container <image_name>
This step starts a Docker container with an NFS volume using docker run -v <server_ip>:/shared:/cntnt_container <image_name>. This command mounts the NFS share /shared on the server (specified by <server_ip>) to the /cntnt_container directory inside the container.

Remember to replace <server_ip> with the IP address of the NFS server and <image_name> with the name of the Docker image you want to run.