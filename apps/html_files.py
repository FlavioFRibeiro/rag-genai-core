css = """
<style>
:root {
  --bot-bg: #7686ad;
  --user-bg: #e8e8e8;
  --bot-text: #ffffff;
  --user-text: #333333;
  --avatar-size: 60px;
  --avatar-radius: 10px;
}

.chat-message {
  display: flex;
  margin-bottom: 1rem;
  padding: 1.5rem;
  border-radius: 0.5rem;
}

.chat-message.user {
  background-color: var(--user-bg);
}

.chat-message.bot {
  background-color: var(--bot-bg);
}

.chat-message .avatar {
  width: 20%;
}

.avatar-badge {
  width: var(--avatar-size);
  height: var(--avatar-size);
  border-radius: var(--avatar-radius);
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
  font-weight: 700;
  font-size: 32px;
}

.avatar-bot {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.3);
}

.avatar-user {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  box-shadow: 0 4px 12px rgba(245, 87, 108, 0.3);
}

.chat-message .message {
  width: 80%;
  padding: 0 1.5rem;
}

.chat-message.bot .message {
  color: var(--bot-text);
}

.chat-message.user .message {
  color: var(--user-text);
}
</style>
"""

bot_template = """
<div class="chat-message bot">
  <div class="avatar">
    <div class="avatar-badge avatar-bot">🤖</div>
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""

user_template = """
<div class="chat-message user">
  <div class="avatar">
    <div class="avatar-badge avatar-user">👤</div>
  </div>
  <div class="message">{{MSG}}</div>
</div>
"""
