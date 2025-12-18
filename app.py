# site-analysisimport streamlit as st
import google.generativeai as genai
from PIL import Image

# --- 1. 页面基础配置 (iPhone 适配关键) ---
st.set_page_config(
    page_title="环境分析 AI",
    page_icon="🌿",
    layout="centered",
    initial_sidebar_state="collapsed" # 手机上默认收起侧边栏
)

# --- 2. CSS 样式美化 (让它看起来像 iOS App) ---
st.markdown("""
    <style>
    /* 全局字体和背景 */
    .stApp {
        background-color: #FAFAFA;
    }
    
    /* 标题样式 */
    h1 {
        font-family: -apple-system, BlinkMacSystemFont, sans-serif;
        color: #1c1c1e;
        font-size: 1.8rem !important;
        text-align: center;
        margin-bottom: 0px;
    }
    
    /* 上传框美化 */
    .stFileUploader {
        background-color: white;
        border-radius: 15px;
        padding: 10px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
    }
    
    /* 按钮美化 - 类似 iOS 的主按钮 */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 50px;
        background-color: #007AFF; /* iOS Blue */
        color: white;
        font-weight: 600;
        font-size: 16px;
        border: none;
    }
    .stButton>button:active {
        background-color: #0056b3;
    }

    /* 去掉 Streamlit 默认的右上角菜单和底部 */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# --- 3. 侧边栏：输入 API Key ---
with st.sidebar:
    st.title("⚙️ 设置")
    api_key = st.text_input("Google Gemini API Key", type="password")
    st.caption("没有 Key? 去 Google AI Studio 申请一个免费的。")
    st.divider()
    st.markdown("Designed for Environmental Design")

# --- 4. 主界面逻辑 ---
st.title("🌿 场地环境分析")
st.markdown("<p style='text-align: center; color: gray; font-size: 0.9em;'>拍照或上传图片，AI 自动生成分析图</p>", unsafe_allow_html=True)

uploaded_file = st.file_uploader("点击上传图片", type=["jpg", "jpeg", "png"], label_visibility="collapsed")

if uploaded_file is not None:
    # 展示用户上传的图
    image = Image.open(uploaded_file)
    st.image(image, caption="原始场地", use_column_width=True)

    # 分析按钮
    if st.button("开始生成分析 (Analyze)"):
        if not api_key:
            st.warning("⚠️ 请点击左上角箭头，在侧边栏填入 API Key")
        else:
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel('gemini-1.5-flash') # 使用 flash 模型，速度快，适合手机

                with st.spinner('AI 正在观察场地...'):
                    # 提示词：要求简短、分点的环境分析
                    prompt = """
                    你是一名专业的环境设计师。请分析这张图片。
                    请用中文，简练地列出以下3点（不要长篇大论，适合手机阅读）：
                    1. ☀️ **光照与风向** (推测)
                    2. 🚶 **动线与视线** (人流分析)
                    3. 🌳 **植物与材质** (现状)
                    最后给出一个改建建议。
                    """
                    response = model.generate_content([prompt, image])
                    
                    st.success("分析完成")
                    
                    # 结果显示框 - 卡片式设计
                    st.markdown(f"""
                    <div style="background-color:white; padding:20px; border-radius:15px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        {response.text}
                    </div>
                    """, unsafe_allow_html=True)
                    
                    st.info("💡 提示：目前 NanoBanana 接口主要返回文字分析。如需叠加箭头图纸，需等待 Google 开放 Imagen 3 编辑接口。")

            except Exception as e:
                st.error(f"出错啦: {e}")
