import streamlit as st
import time
import pandas as pd
from datetime import datetime


# --- 1. 가상 데이터베이스 및 권한 설정 ---
# 형님의 모든 프로젝트 리스트 (Admin 권한용)
ALL_PROJECTS = [
    {"name": "거북목 교정 AI (홍보중)", "url": "https://anti-turtle-neck-ai.streamlit.app/", "category": "Healthcare"},
    {"name": "Biz-Cube AI (서울빅데이터경진대회)", "url": "https://seoul-realty.streamlit.app/", "category": "Real Estate"},
    {"name": "Seoul Realty VIP (한중일 번역서비스)", "url": "https://seoul-realty-vip.streamlit.app/", "category": "Real Estate"},
    {"name": "DoriVac Optimizer (류주희 박사 미팅용)", "url": "https://dorivac-optimizer.streamlit.app/", "category": "Bio"},
    {"name": "SUROP Platform (DoriVac 미팅용)", "url": "https://misatech-surop.streamlit.app/", "category": "Bio"},
    {"name": "Microbiome AI (장항외과 소개)", "url": "https://microbiome-ai-lab.streamlit.app/", "category": "Bio"},
    {"name": "Pet Longevity AI (친구들께 소개)", "url": "https://pet-longevity-ai.streamlit.app/", "category": "Healthcare"},
    {"name": "Pet Longevity AI (영문판,PH홍보중)", "url": "https://pet-longevity.streamlit.app/", "category": "Healthcare"},
    {"name": "Robot Control System (로봇관제)", "url": "https://robot-control.streamlit.app/", "category": "Tech"},
    {"name": "StyleScan: (의류업체 접촉중) ", "url": "https://style-scan-vip1.streamlit.app/", "category": "Fashion"},
    {"name": "StyleScan: (영문판,PH홍보중) ", "url": "https://stylescan-ai.streamlit.app/", "category": "Fashion"},
    {"name": "StyleScan: (내사진,입어볼옷) ", "url": "https://style-scan-vip2.streamlit.app/", "category": "Fashion"},
    {"name": "StyleScan: Fit-Doctor", "url": "https://fit-doctor-pro-v3.streamlit.app/", "category": "Fashion/Healthcare"},
    {"name": "Chef Noir AI (흑백요리사)", "url": "https://bw-chef.streamlit.app/", "category": "Lifestyle/Recipe"},
    {"name": "Chef Noir AI (영문판,PH홍보중)", "url": "https://chef-noir.streamlit.app/", "category": "Lifestyle/Recipe"},
    {"name": "Longevity OS (장수/수명)", "url": "https://longevity-os.streamlit.app/", "category": "Healthcare"},
    {"name": "Smart Pharmacy Solution (약국용)", "url": "https://smart-pharmacy-solution.streamlit.app/", "category": "Medical"},
    {"name": "Church Admin Solution (교회행정용)", "url": "https://church.streamlit.app/", "category": "Church"},
    {"name": "Space Ops C2 (우주로테크 연락요)", "url": "https://space-ops.streamlit.app/", "category": "Defense/Space"},
    {"name": "gilead (제약 임상데이터 분석)", "url": "https://gilead-clinical-ai.streamlit.app/", "category": "Medical"},
    {"name": "oncolytic-virus (항암바이러스 임상데이터 분석)", "url": "https://oncolytic-virus.streamlit.app/", "category": "Medical"},
    {"name": "her2-analysis (Her2-low 환자군 분석)", "url": "https://oncolytic-virus.streamlit.app/", "category": "Medical/미화"},
    {"name": "travel-ai (여행ai 고모부아는곳?)", "url": "https://oncolytic-virus.streamlit.app/", "category": "Travel"},
    {"name": "bi (영수증분석)", "url": "https://bi-strategist.streamlit.app/", "category": "경영회계"},
    {"name": "Error Doctor (에러 해결)", "url": "https://error-doctor.streamlit.app/", "category": "개발자"}
]

# 사용자별 권한 DB
USER_DB = {
    "bslee": {
        "name": "형님 (Administrator)",
        "role": "SuperAdmin",
        "projects": [p["name"] for p in ALL_PROJECTS]
    },
    "200400": {
        "name": "동운인터내셔널 담당자",
        "role": "Client",
        "projects": ["반도체 냉각 모듈 최적화 AI (가상)", "Project Monitoring"]
    }
}

# --- 2. 보안 인디케이터 스타일 정의 ---
st.set_page_config(page_title="AI Business OS - Security Center", layout="wide")

st.markdown("""
    <style>
    .led-green {
        margin: 0 auto;
        width: 15px;
        height: 15px;
        background-color: #ABFF00;
        border-radius: 50%;
        box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #304701 0 -1px 9px, #89FF00 0 2px 12px;
        display: inline-block;
        animation: blinkRed 1.5s infinite;
    }
    @keyframes blinkRed {
        from { background-color: #ABFF00; }
        50% { background-color: #304701; box-shadow: none; }
        to { background-color: #ABFF00; }
    }
    .security-box {
        padding: 20px;
        border-radius: 10px;
        background-color: #f0f2f6;
        border-left: 5px solid #007bff;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 세션 상태 관리 (로그인 시뮬레이션) ---
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
    st.session_state.user_id = None

# --- 4. 메인 화면 로직 ---
if not st.session_state.logged_in:
    st.title("🔒 AI Business OS Login")
    user_input = st.text_input("UserID", placeholder="아이디를 입력하세요")
    if st.button("Login"):
        if user_input in USER_DB:
            st.session_state.logged_in = True
            st.session_state.user_id = user_input
            st.rerun()
        else:
            st.error("등록되지 않은 사용자입니다.")
else:
    user_info = USER_DB[st.session_state.user_id]
    
    # 사이드바: 프로젝트 스위처 및 보안 상태
    with st.sidebar:
        st.title("🛰️ Dashboard")
        st.subheader(f"Welcome, {user_info['name']}")
        st.write(f"Role: **{user_info['role']}**")
        
        st.divider()
        
        # 가시적 보안 인디케이터
        st.markdown('### 🟢 System Status')
        col1, col2 = st.columns([1, 5])
        with col1:
            st.markdown('<div class="led-green"></div>', unsafe_allow_html=True)
        with col2:
            st.write("Local AI Processing")
        st.caption("Data Encrypted & Air-gapped")
        
        st.divider()
        
        # 프로젝트 스위처 (권한 기반)
        selected_project = st.selectbox("📂 Project Switcher", user_info["projects"])
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # 메인 컨텐츠 영역
    tab1, tab2, tab3 = st.tabs(["🚀 Project Console", "🛡️ Security & Governance", "⚙️ Advanced Settings"])

    with tab1:
        st.header(f"Project: {selected_project}")
        
        # 관리자 계정일 경우 URL 연결 및 상세 정보 표시
        if user_info["role"] == "SuperAdmin":
            project_data = next((p for p in ALL_PROJECTS if p["name"] == selected_project), None)
            if project_data:
                st.info(f"분야: {project_data['category']}")
                st.markdown(f"🔗 [서비스 바로가기]({project_data['url']})")
                
                # 프로젝트 상태 모니터링 (더미 데이터)
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Status", "Active", "Running")
                col_b.metric("Data Usage", "1.2GB", "-5%")
                col_c.metric("API Calls", "Local Only", "No External")
        else:
            st.warning("발주처 전용 모니터링 모드입니다. 상세 설계 데이터는 보안 프로토콜에 의해 보호됩니다.")
            st.progress(65, text="Project Progress (Stage 2: Validation)")

    with tab2:
        st.header("🛡️ Security & Governance Center")
        
        st.markdown("""
        <div class="security-box">
        <h4>🔒 Private AI Identity & Access Management</h4>
        본 시스템은 <b>Tenant Isolation (프로젝트 격리)</b> 원칙에 따라 설계되었습니다. 
        모든 데이터 추론은 외부 클라우드가 아닌 전용 로컬 서버에서만 처리됩니다.
        </div>
        """, unsafe_allow_html=True)

    with tab3:
        if user_info["role"] != "SuperAdmin":
            st.warning("⚠️ 이 영역은 SuperAdmin 전용입니다. 접근이 제한됩니다.")
        else:
            st.header("⚙️ Advanced System Configuration")
            
            col_cfg1, col_cfg2 = st.columns(2)
            
            with col_cfg1:
                st.subheader("🤖 AI Engine Tuning")
                model_type = st.selectbox("Inference Model", ["Llama-3-70B (Local)", "Llama-3-8B (Fast)", "Mistral-v0.2"])
                temp = st.slider("Temperature (Creativity)", 0.0, 1.0, 0.2)
                st.caption("낮을수록 정교하고 논리적인 기술 영업 답변을 생성합니다.")
                
                st.divider()
                
                st.subheader("🌐 Network & Security")
                st.toggle("Strict Air-gap Mode", value=True)
                st.toggle("IP Whitelisting (Active)", value=True)
                st.text_input("Allowed Admin IP Range", "211.xxx.xxx.0/24")

            with col_cfg2:
                st.subheader("📊 System Resource Monitor")
                # 실시간 리소스 감시 시뮬레이션
                import numpy as np
                chart_data = pd.DataFrame(np.random.randn(20, 2), columns=['CPU', 'RAM'])
                st.line_chart(chart_data)
                st.caption("Local Server Resource Usage (Simulated)")
                
                st.divider()
                
                st.subheader("🧹 Data Governance")
                st.date_input("Audit Log Retention Until", datetime.now())
                if st.button("Purge Temporary Cache", type="primary"):
                    with st.spinner("Cleaning..."):
                        time.sleep(1)
                        st.success("Cache cleared safely.")

            st.divider()
            
            # Webhook 및 외부 연동 설정 (B2B 확장성)
            st.subheader("🔌 API & Integrations")
            st.text_input("Webhook URL (For ERP/CRM Linkage)", "https://api.dongwoon.com/v1/sync")
            st.write("Current Status: **Standby**")


        
        st.divider()
        
        col_l, col_r = st.columns(2)
        
        with col_l:
            st.subheader("🔑 Data Sovereignty")
            st.write("- **Encryption:** AES-256 (At rest & In transit)")
            st.write("- **Network:** Air-gapped Environment Simulated")
            st.write("- **AI Engine:** Llama-3-Local (No Data Training)")
            
        with col_r:
            st.subheader("🔍 Real-time Integrity")
            st.write(f"현재 접속 IP: `192.168.0.{hash(st.session_state.user_id) % 255}`")
            st.write(f"마지막 보안 점검: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
            st.write("상태: **Safe**")

        st.divider()
        
        st.subheader("📑 Audit Trail (감사 로그)")
        # 감사 로그 생성
        audit_data = [
            {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "User": st.session_state.user_id, "Action": "Login", "Target": "System"},
            {"Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"), "User": st.session_state.user_id, "Action": "Access", "Target": selected_project},
            {"Timestamp": "2026-05-13 14:20:05", "User": "System", "Action": "Encryption", "Target": "DB_Volume_01"},
        ]
        st.table(pd.DataFrame(audit_data))

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Korean Palantir Framework")
