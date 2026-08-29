#!/bin/bash
# md-out-of-chat 截图脚本（依赖 puppeteer-core + chrome-headless-shell）
# 用法：./screenshot.sh <input.html> <output.png> [width=375]

set -e
NODE_DIR="${NODE_DIR:-/tmp/md-shot}"
CHROME="${CHROME:-/root/.cache/puppeteer/chrome-headless-shell/linux-149.0.7827.22/chrome-headless-shell-linux64/chrome-headless-shell}"

if [ ! -x "$CHROME" ]; then
    echo "❌ 找不到 chrome-headless-shell: $CHROME"
    echo "   安装步骤："
    echo "   apt-get install -y libnspr4 libnss3 libatk1.0-0 libatk-bridge2.0-0 libcups2 libdrm2 libxkbcommon0 libxcomposite1 libgbm1 libpango-1.0-0 libcairo2 libxdamage1 libxfixes3 libxrandr2 libasound2 fonts-noto-cjk"
    echo "   npm install --prefix $NODE_DIR puppeteer-core"
    exit 1
fi

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
