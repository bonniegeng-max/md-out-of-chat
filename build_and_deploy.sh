#!/bin/bash
# md2view 构建 + 部署
# 用法：./build_and_deploy.sh demo.md [项目名]
# 
# 流程：
# 1. 检查输入 .md 存在
# 2. 检查 dist 目录
# 3. 复制 index.html（基础样式） + 生成新的 html
# 4. 部署到 web

set -e
SKILL_DIR="$(cd "$(dirname "$0")" && pwd)"
DIST_DIR="$SKILL_DIR/dist"

# 1. 校验参数
if [ -z "$1" ]; then
    echo "用法: $0 <md文件> [项目名]"
    echo "示例: $0 demo.md my-view"
    exit 1
fi

MD_FILE="$1"
if [ ! -f "$MD_FILE" ]; then
    echo "❌ 找不到: $MD_FILE"
    exit 1
fi

# 2. 准备 dist 目录
echo "→ 准备 dist 目录..."
rm -rf "$DIST_DIR"
mkdir -p "$DIST_DIR"

# 3. 生成 html（用脚本）
cd "$SKILL_DIR"
python3 md2share.py "$MD_FILE" "$DIST_DIR/index.html"

# 4. 校验：必须有 index.html
if [ ! -f "$DIST_DIR/index.html" ]; then
    echo "❌ 部署失败：没有生成 index.html"
    exit 1
fi

# 5. 显示
echo "→ 部署准备："
ls -la "$DIST_DIR"
echo "→ index.html 大小: $(wc -c < "$DIST_DIR/index.html" | tr -d ' ') bytes"
echo "✅ 准备完成，下一步：调用 deploy 工具，dist_dir=$DIST_DIR"
