#!/bin/bash
# md-out-of-chat 自动 push 脚本
# 用法：./auto_push.sh "提交信息"
# 环境变量：GITHUB_TOKEN 必填

set -e
TOKEN="${GITHUB_TOKEN:?需要先 export GITHUB_TOKEN=xxx}"
GIT_USER="${GIT_USER:-bonniegeng-max}"
GIT_EMAIL="${GIT_EMAIL:-$GIT_USER@users.noreply.github.com}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cd "$SCRIPT_DIR"

# 1. 初始化仓库（如未）
if [ ! -d ".git" ]; then
    git init -q
    git branch -M main
fi
git config user.name "$GIT_USER"
git config user.email "$GIT_EMAIL"

# 2. .gitignore
cat > .gitignore << 'GI'
# 部署产物
dist/
__pycache__/
*.pyc
.DS_Store
# 敏感（万一你之后放了 token 到本地）
*.token
*.secret
GI

# 3. 远端
git remote remove origin 2>/dev/null || true
git remote add origin "https://$TOKEN@github.com/$GIT_USER/md-out-of-chat.git"

# 4. 提交 + 推送
MSG="${1:-update: 自动同步 $(date +%Y-%m-%d\ %H:%M)}"
git add -A
git commit -m "$MSG" --allow-empty -q
git push -u origin main 2>&1 | tail -3
echo "✅ https://github.com/$GIT_USER/md-out-of-chat"
