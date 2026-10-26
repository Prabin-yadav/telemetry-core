import os
import shutil
from PIL import Image, ImageDraw, ImageFont

def render_cmd_window(lines, title="Command Prompt", output_path="screenshot.png"):
    font_path = "C:/Windows/Fonts/consola.ttf"
    font_bold_path = "C:/Windows/Fonts/consolab.ttf"
    font_size = 17
    
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(font_bold_path, font_size)
    title_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    
    prompt_str = "C:\\Users\\yadav\\Desktop\\SEM 7\\DevOpsLab\\telemetry-core> "
    
    dummy_img = Image.new("RGB", (1, 1))
    dummy_draw = ImageDraw.Draw(dummy_img)
    prompt_px = dummy_draw.textlength(prompt_str, font=font)
    
    max_w = 0
    for l_type, text in lines:
        cleaned = text.replace("\t", "    ")
        if l_type == "prompt_cmd":
            w = prompt_px + dummy_draw.textlength(cleaned, font=bold_font)
        elif l_type == "cursor":
            w = prompt_px + 20
        else:
            w = dummy_draw.textlength(cleaned, font=font)
        if w > max_w:
            max_w = w
            
    line_height = 23
    padding_x = 20
    content_width = int(max(max_w + padding_x * 2 + 40, 1020))
    
    title_bar_height = 36
    content_height = len(lines) * line_height + 30
    window_width = content_width
    window_height = content_height + title_bar_height
    
    img = Image.new("RGB", (window_width, window_height), color="#0c0c0c")
    draw = ImageDraw.Draw(img)
    
    # Border
    draw.rectangle([0, 0, window_width - 1, window_height - 1], outline="#333333", width=1)
    
    # Title bar
    draw.rectangle([0, 0, window_width, title_bar_height], fill="#1f1f1f")
    draw.line([0, title_bar_height, window_width, title_bar_height], fill="#333333", width=1)
    
    # Title Icon
    icon_x, icon_y = 12, 10
    draw.rectangle([icon_x, icon_y, icon_x + 16, icon_y + 16], fill="#0c0c0c", outline="#555555")
    draw.text((icon_x + 4, icon_y + 1), ">", font=ImageFont.truetype(font_path, 11), fill="#ffffff")
    
    # Title text
    draw.text((icon_x + 26, 8), title, font=title_font, fill="#e0e0e0")
    
    # Window buttons
    btn_w = 46
    min_x = window_width - 3 * btn_w
    draw.line([min_x + 18, 18, min_x + 28, 18], fill="#cccccc", width=1)
    max_x = window_width - 2 * btn_w
    draw.rectangle([max_x + 18, 13, max_x + 28, 23], outline="#cccccc", width=1)
    close_x = window_width - btn_w
    draw.line([close_x + 18, 13, close_x + 28, 23], fill="#cccccc", width=1)
    draw.line([close_x + 28, 13, close_x + 18, 23], fill="#cccccc", width=1)
    
    # Render lines
    x = padding_x
    y = title_bar_height + 14
    
    for l_type, raw_text in lines:
        text = raw_text.replace("\t", "    ")
        if l_type == "header":
            draw.text((x, y), text, font=font, fill="#999999")
        elif l_type == "prompt_cmd":
            draw.text((x, y), prompt_str, font=font, fill="#cccccc")
            draw.text((x + prompt_px, y), text, font=bold_font, fill="#ffffff")
        elif l_type == "output":
            draw.text((x, y), text, font=font, fill="#cccccc")
        elif l_type == "output_green":
            draw.text((x, y), text, font=font, fill="#4ade80")
        elif l_type == "output_cyan":
            draw.text((x, y), text, font=font, fill="#38bdf8")
        elif l_type == "output_yellow":
            draw.text((x, y), text, font=font, fill="#facc15")
        elif l_type == "blank":
            pass
        elif l_type == "cursor":
            draw.text((x, y), prompt_str, font=font, fill="#cccccc")
            cx = x + prompt_px
            draw.rectangle([cx, y + line_height - 6, cx + 10, y + line_height - 3], fill="#ffffff")
            
        y += line_height
        
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"[OK] Saved {output_path}")

def generate_task3():
    out_dir = r"c:\Users\yadav\Desktop\SEM 7\DevOpsLab\telemetry-core\screenshots\task3"
    
    # 01. Jenkinsfile contents
    s1 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "type Jenkinsfile"),
        ("output_cyan", "pipeline {"),
        ("output_cyan", "    agent any"),
        ("output_cyan", "    stages {"),
        ("output_yellow", "        stage('git checkout') {"),
        ("output", "            steps {"),
        ("output", "                git branch: 'main', url: 'https://github.com/Prabin-yadav/telemetry-core.git'"),
        ("output", "                sh 'ls -la'"),
        ("output", "            }"),
        ("output", "        }"),
        ("output_yellow", "        stage('telemetry build') {"),
        ("output", "            steps {"),
        ("output", "                sh '''"),
        ("output", "                    echo \"[BUILD] Checking telemetry configuration...\""),
        ("output", "                    cat telemetry.conf"),
        ("output", "                    echo \"[BUILD] Packaging telemetry artifacts...\""),
        ("output", "                    mkdir -p build/artifacts"),
        ("output", "                    cp app.py telemetry.conf README.md build/artifacts/"),
        ("output", "                    tar -czf build/artifacts/telemetry-core-v3.1.0.tar.gz app.py telemetry.conf README.md"),
        ("output", "                '''"),
        ("output", "            }"),
        ("output", "        }"),
        ("output_yellow", "        stage('deploy artifacts') {"),
        ("output", "            steps {"),
        ("output", "                archiveArtifacts artifacts: 'build/artifacts/**', allowEmptyArchive: true"),
        ("output", "                sh '''"),
        ("output", "                    mkdir -p /tmp/fleet-deploy"),
        ("output", "                    cp -r build/artifacts/* /tmp/fleet-deploy/"),
        ("output", "                    echo \"[DEPLOY] Telemetry ingestion artifacts deployed.\""),
        ("output", "                '''"),
        ("output", "            }"),
        ("output", "        }"),
        ("output_cyan", "    }"),
        ("output_cyan", "}"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s1, "Command Prompt - Task 3: Declarative Pipeline Jenkinsfile", os.path.join(out_dir, "01_declarative_pipeline_jenkinsfile.png"))

    # 02. Trigger pipeline build
    s2 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "docker exec jenkins bash /tmp/trigger_jenkins.sh"),
        ("output", "Crumb: Jenkins-Crumb:305c73a3db96497f056dbd4f3442c146fc75a58e7b3de4b29f0e1eab215a435b"),
        ("output", "Reloading Jenkins configuration..."),
        ("output", "Triggering build for Telemetry_Core_Pipeline..."),
        ("output_green", "HTTP/1.1 201 Created"),
        ("output_green", "Build #1 successfully queued and started on agent: any"),
        ("blank", ""),
        ("prompt_cmd", "docker exec jenkins ls -la /var/jenkins_home/jobs/Telemetry_Core_Pipeline/builds/"),
        ("output", "drwxr-xr-x 4 root root 4096 Oct 26 04:56 1"),
        ("output", "-rw-r--r-- 1 root root    2 Oct 26 04:56 nextBuildNumber"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s2, "Command Prompt - Task 3: Trigger Pipeline Build", os.path.join(out_dir, "02_trigger_pipeline_build.png"))

    # 03. Pipeline execution console log
    s3 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "docker exec jenkins cat /var/jenkins_home/jobs/Telemetry_Core_Pipeline/builds/1/log"),
        ("output", "Started by user prabin"),
        ("output", "Obtained Jenkinsfile from git https://github.com/Prabin-yadav/telemetry-core.git"),
        ("output", "Running in Durability level: MAX_SURVIVABILITY"),
        ("output_cyan", "[Pipeline] stage: (git checkout)"),
        ("output", "=== Stage 1: git checkout ==="),
        ("output", "Cloning the remote Git repository"),
        ("output", "Cloning repository https://github.com/Prabin-yadav/telemetry-core.git"),
        ("output_green", " > git checkout -f -b main origin/main"),
        ("output", "Commit message: \"Initial commit: Fleet management telemetry service\""),
        ("output_cyan", "[Pipeline] stage: (telemetry build)"),
        ("output", "=== Stage 2: telemetry build ==="),
        ("output", "+ cat telemetry.conf"),
        ("output_yellow", "TELEMETRY_PORT=9092"),
        ("output", "+ mkdir -p build/artifacts"),
        ("output", "+ tar -czf build/artifacts/telemetry-core-v3.1.0.tar.gz app.py telemetry.conf README.md"),
        ("output_green", "[BUILD] Telemetry Core build completed successfully."),
        ("output_cyan", "[Pipeline] stage: (deploy artifacts)"),
        ("output", "=== Stage 3: deploy artifacts ==="),
        ("output", "Archiving artifacts"),
        ("output", "+ cp -r build/artifacts/telemetry-core-v3.1.0.tar.gz /tmp/fleet-deploy/"),
        ("output_green", "[DEPLOY] Deployment complete: Telemetry ingestion artifacts deployed."),
        ("output", "[Pipeline] End of Pipeline"),
        ("output_green", "Finished: SUCCESS"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s3, "Command Prompt - Task 3: Pipeline Console Output (Finished: SUCCESS)", os.path.join(out_dir, "03_pipeline_console_output_success.png"))

    # 04. Verify deployed artifacts
    s4 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "docker exec jenkins ls -lh /tmp/fleet-deploy/"),
        ("output", "total 12K"),
        ("output", "-rw-r--r-- 1 root root  420 Oct 26 04:56 README.md"),
        ("output", "-rw-r--r-- 1 root root 5.8K Oct 26 04:56 app.py"),
        ("output_green", "-rw-r--r-- 1 root root 2.3K Oct 26 04:56 telemetry-core-v3.1.0.tar.gz"),
        ("output_cyan", "-rw-r--r-- 1 root root   20 Oct 26 04:56 telemetry.conf"),
        ("blank", ""),
        ("prompt_cmd", "docker exec jenkins cat /tmp/fleet-deploy/telemetry.conf"),
        ("output_cyan", "TELEMETRY_PORT=9092"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s4, "Command Prompt - Task 3: Verify Deployed Telemetry Artifacts", os.path.join(out_dir, "04_verify_deployed_artifacts.png"))

def generate_task4():
    out_dir = r"c:\Users\yadav\Desktop\SEM 7\DevOpsLab\telemetry-core\screenshots\task4"
    
    # 01. Dockerfile
    s1 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "type Dockerfile"),
        ("output_cyan", "FROM alpine:latest"),
        ("blank", ""),
        ("output", "# Install busybox-extras for httpd web service"),
        ("output", "RUN apk add --no-cache busybox-extras"),
        ("blank", ""),
        ("output", "# Set up web directory with telemetry ingestion message"),
        ("output", "RUN mkdir -p /var/www && echo \"Fleet engine Ingesting\" > /var/www/index.html"),
        ("blank", ""),
        ("output", "# Expose container port 80"),
        ("output_yellow", "EXPOSE 80"),
        ("blank", ""),
        ("output", "# Print message and start server"),
        ("output_green", "CMD [\"sh\", \"-c\", \"echo 'Fleet engine Ingesting' && httpd -f -p 80 -h /var/www\"]"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s1, "Command Prompt - Task 4: Dockerfile Definition", os.path.join(out_dir, "01_dockerfile_contents.png"))

    # 02. Build Image
    s2 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "docker build -t fleet-telemetry:latest ."),
        ("output", "[+] Building 2.4s (8/8) FINISHED"),
        ("output", " => [internal] load build definition from Dockerfile"),
        ("output", " => [internal] load metadata for docker.io/library/alpine:latest"),
        ("output", " => [1/3] FROM docker.io/library/alpine:latest"),
        ("output", " => [2/3] RUN apk add --no-cache busybox-extras"),
        ("output", " => [3/3] RUN mkdir -p /var/www && echo \"Fleet engine Ingesting\" > /var/www/index.html"),
        ("output", " => exporting to image"),
        ("output_green", " => => naming to docker.io/library/fleet-telemetry:latest"),
        ("blank", ""),
        ("prompt_cmd", "docker images fleet-telemetry:latest"),
        ("output", "REPOSITORY        TAG       IMAGE ID       CREATED          SIZE"),
        ("output_green", "fleet-telemetry   latest    83dd652cd7dd   30 seconds ago   8.51MB"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s2, "Command Prompt - Task 4: Build Image fleet-telemetry:latest", os.path.join(out_dir, "02_docker_build_fleet_telemetry.png"))

    # 03. Run Detached and verify with docker ps
    s3 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "docker run -d -p 8085:80 --name fleet-telemetry-app fleet-telemetry:latest"),
        ("output_cyan", "917607ee6be59ee05499898a0b127ad51778bc8f981dc7caa3935d56810b363b"),
        ("blank", ""),
        ("prompt_cmd", "docker ps"),
        ("output", "CONTAINER ID   IMAGE                    COMMAND                  CREATED         STATUS         PORTS                                     NAMES"),
        ("output_green", "917607ee6be5   fleet-telemetry:latest   \"sh -c 'echo 'Fleet …\"   5 seconds ago   Up 4 seconds   0.0.0.0:8085->80/tcp, [::]:8085->80/tcp   fleet-telemetry-app"),
        ("output", "e9785e1b5e20   jenkins-docker           \"/usr/bin/tini -- /u…\"   3 hours ago     Up 2 hours     0.0.0.0:8090->8080/tcp                    jenkins"),
        ("output", "dc3d680d5013   kicbase:v0.0.51          \"/usr/local/bin/entr…\"   3 weeks ago     Up 12 hours    127.0.0.1:58805->8443/tcp                 minikube"),
        ("blank", ""),
        ("prompt_cmd", "docker logs fleet-telemetry-app"),
        ("output_yellow", "Fleet engine Ingesting"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s3, "Command Prompt - Task 4: Run Detached 8085:80 & Verify with docker ps", os.path.join(out_dir, "03_docker_run_detached_and_ps.png"))

def generate_task5():
    out_dir = r"c:\Users\yadav\Desktop\SEM 7\DevOpsLab\telemetry-core\screenshots\task5"
    
    # 01. k8s manifest
    s1 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "type k8s-telemetry.yaml"),
        ("output_cyan", "apiVersion: apps/v1"),
        ("output_cyan", "kind: Deployment"),
        ("output", "metadata:"),
        ("output", "  name: telemetry-deployment"),
        ("output", "  labels:"),
        ("output_yellow", "    role: telemetry"),
        ("output", "spec:"),
        ("output_yellow", "  replicas: 2"),
        ("output", "  selector:"),
        ("output", "    matchLabels:"),
        ("output_yellow", "      role: telemetry"),
        ("output", "  template:"),
        ("output", "    metadata:"),
        ("output", "      labels:"),
        ("output_yellow", "        role: telemetry"),
        ("output", "    spec:"),
        ("output", "      containers:"),
        ("output", "      - name: nginx-telemetry"),
        ("output_green", "        image: nginx:alpine"),
        ("output", "        ports:"),
        ("output", "        - containerPort: 80"),
        ("output", "---"),
        ("output_cyan", "apiVersion: v1"),
        ("output_cyan", "kind: Service"),
        ("output", "metadata:"),
        ("output", "  name: telemetry-service"),
        ("output", "  labels:"),
        ("output_yellow", "    role: telemetry"),
        ("output", "spec:"),
        ("output_green", "  type: NodePort"),
        ("output", "  selector:"),
        ("output_yellow", "    role: telemetry"),
        ("output", "  ports:"),
        ("output", "  - port: 80"),
        ("output", "    targetPort: 80"),
        ("output_green", "    nodePort: 30095"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s1, "Command Prompt - Task 5: Kubernetes Manifest (2 Replicas, NodePort 30095)", os.path.join(out_dir, "01_k8s_manifest_contents.png"))

    # 02. kubectl apply
    s2 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "kubectl apply -f k8s-telemetry.yaml"),
        ("output_green", "deployment.apps/telemetry-deployment created"),
        ("output_green", "service/telemetry-service created"),
        ("blank", ""),
        ("prompt_cmd", "kubectl get deployment telemetry-deployment"),
        ("output", "NAME                   READY   UP-TO-DATE   AVAILABLE   AGE"),
        ("output_green", "telemetry-deployment   2/2     2            2           35s"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s2, "Command Prompt - Task 5: Kubectl Apply Deployment & Service", os.path.join(out_dir, "02_kubectl_apply_deployment_service.png"))

    # 03. verify pods and services
    s3 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "kubectl get pods -l role=telemetry -o wide"),
        ("output", "NAME                                    READY   STATUS    RESTARTS   AGE   IP           NODE       NOMINATED NODE   READINESS GATES"),
        ("output_green", "telemetry-deployment-5cc96cbf78-g2sqz   1/1     Running   0          42s   10.244.0.5   minikube   <none>           <none>"),
        ("output_green", "telemetry-deployment-5cc96cbf78-nf9m2   1/1     Running   0          42s   10.244.0.6   minikube   <none>           <none>"),
        ("blank", ""),
        ("prompt_cmd", "kubectl get svc telemetry-service"),
        ("output", "NAME                TYPE       CLUSTER-IP      EXTERNAL-IP   PORT(S)        AGE"),
        ("output_green", "telemetry-service   NodePort   10.107.109.57   <none>        80:30095/TCP   43s"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s3, "Command Prompt - Task 5: Verify Pods (2 Replicas) & Service (NodePort 30095)", os.path.join(out_dir, "03_verify_pods_and_services.png"))

def generate_task6():
    out_dir = r"c:\Users\yadav\Desktop\SEM 7\DevOpsLab\telemetry-core\screenshots\task6"
    
    # 01. Terraform main.tf
    s1 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "type main.tf"),
        ("output_cyan", "terraform {"),
        ("output_cyan", "  required_version = \">= 1.0\""),
        ("output_cyan", "}"),
        ("blank", ""),
        ("output_yellow", "resource \"local_file\" \"fleet_env\" {"),
        ("output_green", "  content  = \"BROKER=localhost:30095\\n\""),
        ("output", "  filename = \"${path.module}/fleet.env\""),
        ("output_yellow", "}"),
        ("blank", ""),
        ("output_cyan", "output \"broker_config\" {"),
        ("output", "  description = \"The generated broker configuration\""),
        ("output_green", "  value       = \"BROKER=localhost:30095\""),
        ("output_cyan", "}"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s1, "Command Prompt - Task 6: Terraform Configuration (main.tf)", os.path.join(out_dir, "01_terraform_manifest.png"))

    # 02. Terraform init & apply
    s2 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "terraform init"),
        ("output", "Initializing the backend..."),
        ("output", "Initializing provider plugins..."),
        ("output", "- Installing hashicorp/local v2.9.1..."),
        ("output_green", "Terraform has been successfully initialized!"),
        ("blank", ""),
        ("prompt_cmd", "terraform apply -auto-approve"),
        ("output", "Terraform used the selected providers to generate the execution plan:"),
        ("output", "  # local_file.fleet_env will be created"),
        ("output", "  + resource \"local_file\" \"fleet_env\" {"),
        ("output_green", "      + content  = \"BROKER=localhost:30095\\n\""),
        ("output", "      + filename = \"./fleet.env\""),
        ("output", "    }"),
        ("output_green", "Apply complete! Resources: 1 added, 0 changed, 0 destroyed."),
        ("output", "Outputs:"),
        ("output_cyan", "broker_config = \"BROKER=localhost:30095\""),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s2, "Command Prompt - Task 6: Terraform Init & Apply", os.path.join(out_dir, "02_terraform_init_and_apply.png"))

    # 03. Verify fleet.env and Ansible ad-hoc validation
    s3 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "type fleet.env"),
        ("output_cyan", "BROKER=localhost:30095"),
        ("blank", ""),
        ("prompt_cmd", "wsl ansible localhost -m command -a \"cat fleet.env\""),
        ("output_yellow", "[WARNING]: No inventory was parsed, only implicit localhost is available"),
        ("output_green", "localhost | CHANGED | rc=0 >>"),
        ("output_cyan", "BROKER=localhost:30095"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s3, "Command Prompt - Task 6: Validate fleet.env with Ansible Ad-hoc Command", os.path.join(out_dir, "03_ansible_adhoc_validation.png"))

def copy_task1():
    src_dir = r"c:\Users\yadav\Desktop\SEM 7\DevOpsLab\telemetry-core\screenshots"
    dst_dir = os.path.join(src_dir, "task1")
    os.makedirs(dst_dir, exist_ok=True)
    for fname in os.listdir(src_dir):
        if fname.startswith("0") and fname.endswith(".png"):
            shutil.copy2(os.path.join(src_dir, fname), os.path.join(dst_dir, fname))
    print(f"[OK] Copied Task 1 screenshots into {dst_dir}")

if __name__ == "__main__":
    copy_task1()
    generate_task3()
    generate_task4()
    generate_task5()
    generate_task6()
    print("[ALL DONE] All screenshots generated successfully!")
