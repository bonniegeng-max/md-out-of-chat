#!/bin/bash
# md-out-of-chat 截图脚本（依赖 puppeteer-core + chrome-headless-shell）
# 用法：./screenshot.sh <input.html> <output.png> [width=375]

set -e
NODE_DIR="${NODE_DIR:-/tmp/md-shot}"

# 自动探测 chrome/chromium 可执行文件（CHROME 环境变量优先）
detect_chrome() {
    if [ -n "$CHROME" ] && [ -x "$CHROME" ]; then
        echo "$CHROME"; return 0
    fi
    # macOS 常规安装位置
    for p in \
        "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
        "/Applications/Chromium.app/Contents/MacOS/Chromium" \
        "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge" \
        "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser"; do
        if [ -x "$p" ]; then echo "$p"; return 0; fi
    done
    # puppeteer 缓存（Linux: ~/.cache/puppeteer，macOS: ~/Library/Caches/puppeteer）
    for cache_dir in "$HOME/.cache/puppeteer" "$HOME/Library/Caches/puppeteer"; do
        if [ -d "$cache_dir" ]; then
            p=$(find "$cache_dir" -type f \( -name 'chrome' -o -name 'chrome-headless-shell' -o -name 'Google Chrome for Testing' \) 2>/dev/null | head -1)
            if [ -n "$p" ] && [ -x "$p" ]; then echo "$p"; return 0; fi
        fi
    done
    # PATH 里找
    for c in google-chrome google-chrome-stable chromium chromium-browser chrome; do
        if command -v "$c" >/dev/null 2>&1; then command -v "$c"; return 0; fi
    done
    return 1
}

CHROME="$(detect_chrome)" || CHROME=""

if [ -z "$CHROME" ]; then
    echo "❌ 找不到 Chrome/Chromium，按顺序尝试过："
    echo "   1. CHROME 环境变量"
    echo "   2. /Applications 下的 Chrome/Chromium/Edge/Brave（macOS）"
    echo "   3. puppeteer 缓存目录"
    echo "   4. PATH 中的 chrome 命令"
    echo "   可手动指定：CHROME=/path/to/chrome ./screenshot.sh ..."
    echo ""
    echo "   Linux 依赖安装："
    echo "   apt-get install -y libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libgbm1 libpango-1.0-0 libcairo2 libxdamage1 libxfixes3 libxrandr2 libasound2 fonts-noto-cjk"
    exit 1
fi
echo "→ 使用浏览器: $CHROME"

if [ ! -d "$NODE_DIR" ]; then
    echo "❌ 找不到 node 模块: $NODE_DIR"
    echo "   安装：npm install --prefix $NODE_DIR puppeteer-core"
    exit 1
fi

INPUT="$1"
OUTPUT="$2"
WIDTH="${3:-375}"

if [ -z "$INPUT" ] || [ -z "$OUTPUT" ]; then
    echo "用法: ./screenshot.sh <input.html> <output.png> [width=375]"
    exit 1
fi

INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
OUTPUT_ABS="$(cd "$(dirname "$OUTPUT")" && pwd)/$(basename "$OUTPUT")"

cd "$NODE_DIR"
node -e "
const puppeteer = require('puppeteer-core');
(async () => {
  const browser = await puppeteer.launch({
    executablePath: '$CHROME',
    headless: 'shell',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage', '--disable-background-networking']
  });
  const page = await browser.newPage();
  // 阻断所有外部网络请求，确保本地 HTML 渲染不会拉取远程资源
  await page.setRequestInterception(true);
  page.on('request', req => {
    const url = req.url();
    if (url.startsWith('file://')) { req.continue(); }
    else { req.abort('blockedbyclient'); }
  });
  await page.setViewport({ width: parseInt('$WIDTH'), height: 800, deviceScaleFactor: 2 });
  await page.goto('file://$INPUT_ABS', { waitUntil: 'load' });
  await page.screenshot({ path: '$OUTPUT_ABS', fullPage: true });
  await browser.close();
  console.log('✅ 截图完成: $OUTPUT_ABS');
})();
"
