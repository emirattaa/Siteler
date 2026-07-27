import os
from PIL import Image

def generate_html():
    gif_path = "me/gif/kedi.gif"
    output_html_path = "me/index.html"
    
    if not os.path.exists(gif_path):
        print(f"Hata: {gif_path} bulunamadı!")
        return

    im = Image.open(gif_path)
    # Raw string kullanarak kaçış karakteri sorununu önlüyoruz
    ascii_density = r" .'`^\",:;Il!i><~+_-?][}{1)(|/tfjrxnuvczXYUJCLQ0OZmwqpdbkhao*#MW&8%B@$"
    
    frames_data = []
    width = 70  # Performans ve boyut dengesi için genişlik
    
    try:
        while True:
            w, h = im.size
            ratio = h / w
            new_h = int(width * ratio * 0.45) # Font oranını eşitlemek için
            
            # GIF karesini RGB moduna çevirip boyutlandırıyoruz
            frame_rgb = im.copy().convert("RGB").resize((width, new_h))
            
            frame_html = ""
            for y in range(new_h):
                for x in range(width):
                    r, g, b = frame_rgb.getpixel((x, y))
                    
                    # Karakter seçimi için parlaklık hesabı (Grayscale formülü)
                    brightness = int(0.299 * r + 0.587 * g + 0.114 * b)
                    char_idx = int(brightness / 255 * (len(ascii_density) - 1))
                    char = ascii_density[char_idx]
                    
                    # HTML özel karakter güvenlik koruması
                    if char == "<": char_esc = "&lt;"
                    elif char == ">": char_esc = "&gt;"
                    elif char == "&": char_esc = "&amp;"
                    else: char_esc = char
                    
                    if char == " ":
                        frame_html += " "
                    else:
                        # Orijinal piksel rengiyle span sarmalama
                        frame_html += f'<span style="color:rgb({r},{g},{b})">{char_esc}</span>'
                frame_html += "\n"
                    
            duration = im.info.get('duration', 100)
            if duration < 20: 
                duration = 100
                
            frames_data.append({
                "text": frame_html,
                "delay": duration
            })
            
            im.seek(im.tell() + 1)
    except EOFError:
        pass

    frames_json = str(frames_data)

    html_content = f"""<!DOCTYPE html>
<html lang="tr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>emirattaa@dev: ~</title>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    
    <style>
        :root {{
            --bg-main: #0d1117;
            --bg-surface: #161b22;
            --bg-highlight: #21262d;
            --text-main: #c9d1d9;
            --text-muted: #8b949e;
            --accent-blue: #58a6ff;
            --accent-green: #3fb950;
            --accent-red: #f85149;
            --accent-yellow: #d29922;
            --border-color: #30363d;
        }}

        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            background-color: var(--bg-main);
            color: var(--text-main);
            font-family: 'JetBrains Mono', monospace;
            line-height: 1.6;
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}

        .dashboard {{
            width: 100%;
            max-width: 1200px;
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
        }}

        .panel {{
            background-color: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: 12px;
            overflow: hidden;
            box-shadow: 0 10px 30px rgba(0,0,0,0.5);
            display: flex;
            flex-direction: column;
        }}

        .panel-header {{
            background-color: var(--bg-highlight);
            padding: 12px 16px;
            border-bottom: 1px solid var(--border-color);
            display: flex;
            align-items: center;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-muted);
        }}

        .window-controls {{
            display: flex;
            gap: 8px;
        }}

        .ctrl {{
            width: 12px;
            height: 12px;
            border-radius: 50%;
        }}
        .ctrl-close {{ background-color: var(--accent-red); }}
        .ctrl-min {{ background-color: var(--accent-yellow); }}
        .ctrl-max {{ background-color: var(--accent-green); }}

        .panel-body {{
            padding: 24px;
            flex: 1;
            overflow-y: auto;
        }}

        .cmd-line {{
            margin-bottom: 16px;
            font-size: 0.9rem;
        }}
        .prompt {{ color: var(--accent-green); font-weight: 500; }}
        .path {{ color: var(--accent-blue); font-weight: 500; }}
        .cmd {{ color: var(--text-main); }}
        .output {{ 
            color: var(--text-muted); 
            margin-top: 4px;
            padding-left: 12px;
            border-left: 2px solid var(--border-color);
        }}
        .output-highlight {{ color: var(--accent-blue); }}
        
        .tag-group {{
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-top: 8px;
        }}
        .tag {{
            background-color: var(--bg-highlight);
            border: 1px solid var(--border-color);
            padding: 2px 8px;
            border-radius: 4px;
            font-size: 0.8rem;
            color: var(--text-main);
        }}

        .ascii-wrapper {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 100%;
            background-color: #000;
            border-radius: 6px;
            padding: 16px;
            position: relative;
            overflow: hidden;
            min-height: 240px;
        }}

        #ascii-display {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 5.5px;
            line-height: 5.5px;
            white-space: pre;
            text-align: center;
        }}

        .status-bar {{
            margin-top: auto;
            width: 100%;
            display: flex;
            justify-content: space-between;
            font-size: 0.75rem;
            color: var(--text-muted);
            border-top: 1px dashed var(--border-color);
            padding-top: 12px;
            margin-top: 16px;
        }}

        #anim-status {{ color: var(--accent-green); font-weight: bold; }}
        .frame-counter {{ font-variant-numeric: tabular-nums; }}

        .links-menu {{
            display: flex;
            flex-direction: column;
            gap: 8px;
            margin-top: 24px;
        }}

        .nav-link {{
            display: flex;
            align-items: center;
            gap: 12px;
            padding: 10px 16px;
            background-color: transparent;
            border: 1px solid var(--border-color);
            color: var(--text-main);
            text-decoration: none;
            border-radius: 6px;
            transition: all 0.2s;
            font-size: 0.9rem;
        }}

        .nav-link:hover {{
            background-color: var(--bg-highlight);
            border-color: var(--accent-blue);
            color: var(--accent-blue);
            transform: translateX(4px);
        }}

        .nav-link i {{ font-size: 1.1rem; }}

        @media (max-width: 900px) {{
            .dashboard {{ grid-template-columns: 1fr; }}
            #ascii-display {{ font-size: 4px; line-height: 4px; }}
            body {{ padding: 1rem; }}
        }}
    </style>
</head>
<body>

    <div class="dashboard">
        
        <!-- SOL PANEL -->
        <div class="panel">
            <div class="panel-header">
                <div class="window-controls">
                    <div class="ctrl ctrl-close"></div>
                    <div class="ctrl ctrl-min"></div>
                    <div class="ctrl ctrl-max"></div>
                </div>
                <span>burak@s24-ultra:~</span>
            </div>
            
            <div class="panel-body">
                <div class="cmd-line">
                    <div><span class="prompt">emirattaa@admin</span>:<span class="path">~</span>$ <span class="cmd">whoami</span></div>
                    <div class="output">Emir</div>
                </div>

                <div class="cmd-line">
                    <div><span class="prompt">burak@admin</span>:<span class="path">~</span>$ <span class="cmd">cat education.txt</span></div>
                    <div class="output">
                        - 8. Sınıf Öğrencisi<br>
                        <span class="output-highlight"></span>
                    </div>
                </div>

                <div class="cmd-line">
                    <div><span class="prompt">burak@admin</span>:<span class="path">~</span>$ <span class="cmd">systemctl status dev-environment</span></div>
                    <div class="output">
                       ● Diller:<br>
                        <div class="tag-group">
                            <span class="tag">JavaScript</span>
                            <span class="tag">Python</span>
                            <span class="tag">Luau</span>
                            <span class="tag">HTML/CSS</span>
                        </div>
                    </div>
                </div>

                <div class="cmd-line">
                    <div><span class="prompt">burak@admin</span>:<span class="path">~</span>$ <span class="cmd">./fetch-projects.sh</span></div>
                    <div class="output">
                        > Sunucular: GitHub & Render<br>
                        > Ekip: <span class="output-highlight">Rizza</span>, <span class="output-highlight">Emoc</span> & Burak
                    </div>
                </div>

                <div class="cmd-line">
                    <div><span class="prompt">burak@admin</span>:<span class="path">~</span>$ <span class="cmd">grep "hobbies" user.config</span></div>
                    <div class="output">                    </div>
                </div>

                <div class="links-menu">
                    <a href="https://github.com/emirattaa" target="_blank" class="nav-link">
                        <i class="fa-brands fa-github"></i> <span>GitHub Profili / Bot Repoları</span>
                    </a>
                    <a href="https://instagram.com/emirattaa" target="_blank" class="nav-link">
                        <i class="fa-brands fa-instagram"></i> <span>Instagram Adresim</span>
                    </a>
                    <a href="https://giphy.com/emirattaa" target="_blank" class="nav-link">
                        <i class="fa-solid fa-film"></i> <span>GIPHY Sticker Koleksiyonu</span>
                    </a>
                    <a href="mailto:dincemirata@gmail.com" class="nav-link">
                        <i class="fa-solid fa-envelope"></i> <span>Gmail İle İletişim</span>
                    </a>
                </div>
            </div>
        </div>

        <!-- SAĞ PANEL -->
        <div class="panel">
            <div class="panel-header">
                <span>./gif/kedi.gif [RGB Color ASCII]</span>
                <span class="frame-counter" id="frame-info">Frame: --/--</span>
            </div>
            
            <div class="panel-body" style="display: flex; flex-direction: column;">
                <div class="ascii-wrapper">
                    <pre id="ascii-display">Yükleniyor...</pre>
                </div>
                
                <div class="status-bar">
                    <span id="anim-status">HAZIR (RENKLİ)</span>
                    <span>Mod: RGB Truecolor</span>
                </div>
            </div>
        </div>

    </div>

    <script>
        const asciiFrames = {frames_json};

        document.addEventListener('DOMContentLoaded', () => {{
            const asciiDisplay = document.getElementById('ascii-display');
            const frameInfo = document.getElementById('frame-info');
            let currentFrameIndex = 0;

            function playAnimation() {{
                if (asciiFrames.length === 0) return;
                
                const currentFrame = asciiFrames[currentFrameIndex];
                // innerHTML kullanarak renklendirilmiş span etiketlerini ekrana basıyoruz
                asciiDisplay.innerHTML = currentFrame.text;
                frameInfo.textContent = `Frame: ${{currentFrameIndex + 1}}/${{asciiFrames.length}}`;
                
                currentFrameIndex = (currentFrameIndex + 1) % asciiFrames.length;
                
                setTimeout(playAnimation, currentFrame.delay);
            }}

            playAnimation();
        }});
    </script>
</body>
</html>
"""

    with open(output_html_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Başarıyla oluşturuldu: {output_html_path}")

if __name__ == "__main__":
    generate_html()
