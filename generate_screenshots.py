import os
from PIL import Image, ImageDraw, ImageFont

def render_cmd_window(lines, title="Command Prompt", output_path="screenshot.png"):
    font_path = "C:/Windows/Fonts/consola.ttf"
    font_bold_path = "C:/Windows/Fonts/consolab.ttf"
    font_size = 17
    
    font = ImageFont.truetype(font_path, font_size)
    bold_font = ImageFont.truetype(font_bold_path, font_size)
    title_font = ImageFont.truetype("C:/Windows/Fonts/segoeui.ttf", 13)
    
    prompt_str = "C:\\Users\\yadav\\Desktop\\SEM 7\\DevOpsLab\\telemetry-core> "
    
    # Calculate dimensions accurately using getlength
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
    
    # Create main image
    img = Image.new("RGB", (window_width, window_height), color="#0c0c0c")
    draw = ImageDraw.Draw(img)
    
    # Window border
    draw.rectangle([0, 0, window_width - 1, window_height - 1], outline="#333333", width=1)
    
    # Title bar
    draw.rectangle([0, 0, window_width, title_bar_height], fill="#1f1f1f")
    draw.line([0, title_bar_height, window_width, title_bar_height], fill="#333333", width=1)
    
    # Title Icon (Windows Terminal / CMD style)
    icon_x, icon_y = 12, 10
    draw.rectangle([icon_x, icon_y, icon_x + 16, icon_y + 16], fill="#0c0c0c", outline="#555555")
    draw.text((icon_x + 4, icon_y + 1), ">", font=ImageFont.truetype(font_path, 11), fill="#ffffff")
    
    # Title text
    draw.text((icon_x + 26, 8), title, font=title_font, fill="#e0e0e0")
    
    # Window buttons
    btn_w = 46
    # Minimize
    min_x = window_width - 3 * btn_w
    draw.line([min_x + 18, 18, min_x + 28, 18], fill="#cccccc", width=1)
    # Maximize
    max_x = window_width - 2 * btn_w
    draw.rectangle([max_x + 18, 13, max_x + 28, 23], outline="#cccccc", width=1)
    # Close
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
            # Windows CMD underline cursor
            draw.rectangle([cx, y + line_height - 6, cx + 10, y + line_height - 3], fill="#ffffff")
            
        y += line_height
        
    os.makedirs(os.path.dirname(os.path.abspath(output_path)), exist_ok=True)
    img.save(output_path, "PNG")
    print(f"[OK] Saved {output_path}")

def generate_all():
    out_dir = r"c:\Users\yadav\Desktop\SEM 7\DevOpsLab\telemetry-core\screenshots"
    
    # 01. Init repo and initial commit
    s1 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "git init"),
        ("output", "Reinitialized existing Git repository in C:/Users/yadav/Desktop/SEM 7/DevOpsLab/telemetry-core/.git/"),
        ("blank", ""),
        ("prompt_cmd", "git status"),
        ("output", "On branch main"),
        ("output", "No commits yet"),
        ("output", "Untracked files:"),
        ("output", "  (use \"git add <file>...\" to include in what will be committed)"),
        ("output_yellow", "    .gitignore"),
        ("output_yellow", "    README.md"),
        ("output_yellow", "    app.py"),
        ("output", "nothing added to commit but untracked files present (use \"git add\" to track)"),
        ("blank", ""),
        ("prompt_cmd", "git add app.py README.md .gitignore"),
        ("prompt_cmd", "git commit -m \"Initial commit: Fleet management telemetry service\""),
        ("output", "[main (root-commit) 0af8cbc] Initial commit: Fleet management telemetry service"),
        ("output", " 3 files changed, 165 insertions(+)"),
        ("output", " create mode 100644 .gitignore"),
        ("output", " create mode 100644 README.md"),
        ("output", " create mode 100644 app.py"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s1, "Command Prompt - Step 1: Initialize Repository and Initial Commit", os.path.join(out_dir, "01_init_repo_and_initial_commit.png"))

    # 02. Create branch 'release v3.1' (release-v3.1) and commit telemetry.conf
    s2 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "git checkout -b release-v3.1"),
        ("output", "Switched to a new branch 'release-v3.1'"),
        ("blank", ""),
        ("prompt_cmd", "echo TELEMETRY_PORT=9092 > telemetry.conf"),
        ("prompt_cmd", "type telemetry.conf"),
        ("output_cyan", "TELEMETRY_PORT=9092"),
        ("blank", ""),
        ("prompt_cmd", "git add telemetry.conf"),
        ("prompt_cmd", "git commit -m \"commit 'telemetry.conf'(TELEMETRY_PORT=9092)\""),
        ("output", "[release-v3.1 94c63f5] commit 'telemetry.conf'(TELEMETRY_PORT=9092)"),
        ("output", " 1 file changed, 1 insertion(+)"),
        ("output", " create mode 100644 telemetry.conf"),
        ("blank", ""),
        ("prompt_cmd", "git status"),
        ("output", "On branch release-v3.1"),
        ("output", "nothing to commit, working tree clean"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s2, "Command Prompt - Step 2: Create Branch release-v3.1 & Commit telemetry.conf", os.path.join(out_dir, "02_create_branch_and_commit_telemetry_conf.png"))

    # 03. Merge release-v3.1 to main
    s3 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "git checkout main"),
        ("output", "Switched to branch 'main'"),
        ("blank", ""),
        ("prompt_cmd", "git merge release-v3.1"),
        ("output", "Merge made by the 'ort' strategy."),
        ("output", " telemetry.conf | 1 +"),
        ("output", " 1 file changed, 1 insertion(+)"),
        ("output", " create mode 100644 telemetry.conf"),
        ("blank", ""),
        ("prompt_cmd", "type telemetry.conf"),
        ("output_cyan", "TELEMETRY_PORT=9092"),
        ("blank", ""),
        ("prompt_cmd", "git branch -a"),
        ("output_green", "* main"),
        ("output", "  release-v3.1"),
        ("output", "  release/v3.1"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s3, "Command Prompt - Step 3: Merge Branch to main", os.path.join(out_dir, "03_merge_release_to_main.png"))

    # 04. Tag v3.1.0-release and verify git log
    s4 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "git tag -a v3.1.0-release -m \"Release v3.1.0\""),
        ("blank", ""),
        ("prompt_cmd", "git tag -n"),
        ("output_green", "v3.1.0-release  Release v3.1.0"),
        ("blank", ""),
        ("prompt_cmd", "git log --graph --oneline --all"),
        ("output_cyan", "*   97e2856 (HEAD -> main, tag: v3.1.0-release) Merge branch 'release-v3.1' into main"),
        ("output_cyan", "|\\  "),
        ("output_cyan", "| * 94c63f5 (release-v3.1, release/v3.1) commit 'telemetry.conf'(TELEMETRY_PORT=9092)"),
        ("output_cyan", "|/  "),
        ("output_cyan", "* 0af8cbc Initial commit: Fleet management telemetry service"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s4, "Command Prompt - Step 4: Tag v3.1.0-release & Verify Commit Tree", os.path.join(out_dir, "04_tag_v3.1.0_release_and_log.png"))

    # 05. Run app.py to verify fleet management telemetry ingestion service
    s5 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "python app.py"),
        ("output", ""),
        ("output_cyan", "======================================================================"),
        ("output_cyan", "  WELCOME TO FLEET MANAGEMENT - VEHICLE TELEMETRY INGESTION SERVICE   "),
        ("output_cyan", "======================================================================"),
        ("output", " [SERVICE]     telemetry-core"),
        ("output", " [VERSION]     v3.1.0-release"),
        ("output", " [CONFIG]      telemetry.conf"),
        ("output_yellow", " [PORT]        9092"),
        ("output_green", " [STATUS]      READY FOR DISTRIBUTED INGESTION"),
        ("output_cyan", "======================================================================"),
        ("blank", ""),
        ("output", "[*] Starting Telemetry Core Service on http://0.0.0.0:9092 ..."),
        ("output", " * Serving Flask app 'app'"),
        ("output", " * Debug mode: off"),
        ("output_green", " * Running on http://127.0.0.1:9092"),
        ("output_green", " * Running on http://192.168.1.10:9092"),
        ("output", "Press CTRL+C to quit"),
        ("blank", "")
    ]
    render_cmd_window(s5, "Command Prompt - Step 5: Run Fleet Management Ingestion Service", os.path.join(out_dir, "05_run_telemetry_app.png"))

    # 06. Push to remote repository (GitHub)
    s6 = [
        ("header", "Microsoft Windows [Version 10.0.22631.4317]"),
        ("header", "(c) Microsoft Corporation. All rights reserved."),
        ("blank", ""),
        ("prompt_cmd", "git remote -v"),
        ("output", "origin  https://github.com/Prabin-yadav/telemetry-core.git (fetch)"),
        ("output", "origin  https://github.com/Prabin-yadav/telemetry-core.git (push)"),
        ("blank", ""),
        ("prompt_cmd", "git push -u origin main --tags"),
        ("output", "branch 'main' set up to track 'origin/main'."),
        ("output", "To https://github.com/Prabin-yadav/telemetry-core.git"),
        ("output_green", " * [new branch]      main -> main"),
        ("output_green", " * [new branch]      release-v3.1 -> release-v3.1"),
        ("output_green", " * [new branch]      release/v3.1 -> release/v3.1"),
        ("output_green", " * [new tag]         v3.1.0-release -> v3.1.0-release"),
        ("blank", ""),
        ("cursor", "")
    ]
    render_cmd_window(s6, "Command Prompt - Step 6: Git Push to GitHub Remote", os.path.join(out_dir, "06_git_push_remote.png"))

if __name__ == "__main__":
    generate_all()
