# cognos install process

### wsl 

 - (https://ubuntu.com/tutorials/enabling-gpu-acceleration-on-ubuntu-on-wsl2-with-the-nvidia-cuda-platform#2-install-the-appropriate-windows-vgpu-driver-for-wsl)

```
wsl -d Ubuntu-22.04  /  wsl --setdefault Ubuntu-22.04
cd ~
sudo apt update -y && sudo apt full-upgrade -y && sudo apt autoremove -y && sudo apt clean -y && sudo apt autoclean -y
sudo apt install wget
wget https://repo.anaconda.com/miniconda/Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
chmod +x Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
./Miniconda3-py310_23.5.2-0-Linux-x86_64.sh
exit
wsl -d Ubuntu-22.04
cd ~
sudo apt-get install build-essential && sudo apt-get install manpages-dev
sudo apt install build-essential libglvnd-dev pkg-config
sudo apt upgrade -y  //sudo apt install --fix-broken -y
conda install conda
conda update conda
conda create -n 3ten python="3.10"
conda install pip
conda update pip
conda deactivate
wget -qO- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.4/install.sh | bash
mkdir chrome
cd chrome
sudo wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo apt install --fix-broken -y
sudo dpkg -i google-chrome-stable_current_amd64.deb
sudo apt-key del 7fa2af80
wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
sudo apt-key adv --fetch-keys https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/3bf863cc.pub
sudo add-apt-repository 'deb https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/ /'
[return]
sudo apt-get update
sudo apt-get -y install cuda
sudo reboot
wsl
cd ~
conda activate 3ten
pip3 install --pre torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/cu121
conda install cudatoolkit
apt get update -y
apt get upgrade -y
sudo reboot
```

# ---
git clone https://github.com/oobabooga/text-generation-webui
cd text-generation-webui
pip install -r requirements.txt
pip install bitsandbytes==0.38.1
// RUN echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/opt/conda/lib/' >> ~/.bashrc
// export LD_LIBRARY_PATH=/usr/lib/wsl/lib:/lib/x86_64-linux-gnu:$LD_LIBRARY_PATH
// https://github.com/oobabooga/text-generation-webui/issues/400
Start over
conda deactivate
conda remove -n textgen --all
conda create -n textgen python=3.10.9
conda activate textgen
pip3 install torch torchvision torchaudio
cd text-generation-webui
pip install -r requirements.txt
cd /home/yourname/miniconda3/envs/textgen/lib/python3.10/site-packages/bitsandbytes/
cp libbitsandbytes_cuda120.so libbitsandbytes_cpu.so
cd -
python server.py --listen --model llama2.7b.llongma.ggml_v3.q4_K_M.bin --lora alpaca-lora-7b  --load-in-8bit
# ---
// https://localai.io/basics/getting_started/
git clone https://github.com/go-skynet/LocalAI
cd LocalAI
cp your-model.bin models/
docker-compose up -d --pull always
// docker-compose down --volumes - periodically 
// docker run --rm -ti --gpus all -p 8080:8080 -e DEBUG=true -e MODELS_PATH=/models -e PRELOAD_MODELS='[{"url": "github:go-skynet/model-gallery/openllama_7b.yaml", "name": "gpt-3.5-turbo", "overrides": { "f16":true, "gpu_layers": 35, "mmap": true, "batch": 512 } } ]' -e THREADS=1 -e BUILD_TYPE=cublas -v $PWD/models:/models quay.io/go-skynet/local-ai:v0.19.0-cublas-cuda12
```

### windows11

win11 ult (hypervisor, wsl)
>enable windows sandbox in (windows) device features
>install scoop and powershell


```
https://learn.microsoft.com/en-us/windows/powertoys/text-extractor
    """ snipping tool OCR char recognition native in-windows eng-US (admin powershell):
    $Capability = Get-WindowsCapability -Online | Where-Object { $_.Name -Like 'Language.OCR*en-US*' }
    $Capability | Remove-WindowsCapability -Online
    """
```


### jupyter-jax

### windows_sandbox

### osx_docker

### git

### cognos/etc.


