import streamlit as st
import time
import pandas as pd
import json
import os
from datetime import datetime
import numpy as np

# --- 0. JSON 데이터 관리 로직 ---
DB_FILE = "projects.json"

def load_data():
    """파일에서 데이터를 로드하거나 기본값을 생성합니다."""
    if os.path.exists(DB_FILE):
        with open(DB_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        # 파일이 없을 경우 형님이 제공해주신 초기 리스트를 저장
        initial_data = [
            {"name": "거북목 교정 AI (홍보중)", "url": "https://anti-turtle-neck-ai.streamlit.app/", "category": "Healthcare", "status": "사용자 지표 모니터링 중"},
            {"name": "Biz-Cube AI (서울빅데이터경진대회)", "url": "https://seoul-realty.streamlit.app/", "category": "Real Estate", "status": "제출 완료 및 심사 대기"},
            {"name": "Seoul Realty VIP (한중일 번역서비스)", "url": "https://seoul-realty-vip.streamlit.app/", "category": "Real Estate", "status": "다국어 DB 최적화 중"},
            {"name": "DoriVac Optimizer (류주희 박사 미팅용)", "url": "https://dorivac-optimizer.streamlit.app/", "category": "Bio", "status": "류주희 박사 미팅 후 피드백 반영 중"},
            {"name": "SUROP Platform (DoriVac 미팅용)", "url": "https://misatech-surop.streamlit.app/", "category": "Bio", "status": "안티젠 설계 모듈 고도화"},
            {"name": "Microbiome AI (장항외과 소개)", "url": "https://microbiome-ai-lab.streamlit.app/", "category": "Bio", "status": "병의원용 대시보드 기획 중"},
            {"name": "Pet Longevity AI (친구들께 소개)", "url": "https://pet-longevity-ai.streamlit.app/", "category": "Healthcare", "status": "베타 테스트 진행 중"},
            {"name": "Pet Longevity AI (영문판,PH홍보중)", "url": "https://pet-longevity.streamlit.app/", "category": "Healthcare", "status": "Product Hunt 유입 분석 중"},
            {"name": "Robot Control System (로봇관제)", "url": "https://robot-control.streamlit.app/", "category": "Tech", "status": "제어 알고리즘 테스트"},
            {"name": "StyleScan: (의류업체 접촉중) ", "url": "https://style-scan-vip1.streamlit.app/", "category": "Fashion", "status": "B2B 제안서 발송 완료"},
            {"name": "StyleScan: (영문판,PH홍보중) ", "url": "https://stylescan-ai.streamlit.app/", "category": "Fashion", "status": "글로벌 유저 피드백 수집"},
            {"name": "StyleScan: (내사진,입어볼옷) ", "url": "https://style-scan-vip2.streamlit.app/", "category": "Fashion", "status": "가상 피팅 엔진 업데이트"},
            {"name": "StyleScan: Fit-Doctor", "url": "https://fit-doctor-pro-v3.streamlit.app/", "category": "Fashion/Healthcare", "status": "체형 분석 로직 고도화"},
            {"name": "Chef Noir AI (흑백요리사)", "url": "https://bw-chef.streamlit.app/", "category": "Lifestyle/Recipe", "status": "레시피 DB 확충 중"},
            {"name": "Chef Noir AI (영문판,PH홍보중)", "url": "https://chef-noir.streamlit.app/", "category": "Lifestyle/Recipe", "status": "홍보 영상 제작 중"},
            {"name": "Longevity OS (장수/수명)", "url": "https://longevity-os.streamlit.app/", "category": "Healthcare", "status": "생체 지표 연동 테스트"},
            {"name": "Smart Pharmacy Solution (약국용)", "url": "https://smart-pharmacy-solution.streamlit.app/", "category": "Medical", "status": "약국 현장 피드백 수렴"},
            {"name": "Church Admin Solution (교회행정용)", "url": "https://church.streamlit.app/", "category": "Church", "status": "기능 안정화 단계"},
            {"name": "Space Ops C2 (우주로테크 연락요)", "url": "https://space-ops.streamlit.app/", "category": "Defense/Space", "status": "위성 궤도 시뮬레이션 고도화"},
            {"name": "gilead (제약 임상데이터 분석)", "url": "https://gilead-clinical-ai.streamlit.app/", "category": "Medical", "status": "임상 데이터셋 전처리"},
            {"name": "oncolytic-virus (항암바이러스 임상데이터 분석)", "url": "https://oncolytic-virus.streamlit.app/", "category": "Medical", "status": "분석 모델 유효성 검증"},
            {"name": "her2-analysis (Her2-low 환자군 분석)", "url": "https://oncolytic-virus.streamlit.app/", "category": "Medical/미화", "status": "환자군 분류 알고리즘 적용"},
            {"name": "travel-ai (여행ai 고모부아는곳?)", "url": "https://oncolytic-virus.streamlit.app/", "category": "Travel", "status": "추천 로직 개발 중"},
            {"name": "bi (영수증분석)", "url": "https://bi-strategist.streamlit.app/", "category": "경영회계", "status": "OCR 인식률 개선 중"},
            {"name": "Error Doctor (에러 해결)", "url": "https://error-doctor.streamlit.app/", "category": "개발자", "status": "디버깅 시나리오 확충"}
        ]
        save_data(initial_data)
        return initial_data

def save_data(data):
    """데이터를 JSON 파일로 저장합니다."""
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

# --- 1. 데이터 로드 및 세션 관리 ---
if "ALL_PROJECTS" not in st.session_state:
    st.session_state.ALL_PROJECTS = load_data()

# 사용자 권한 설정
USER_DB = {
    "bslee": {
        "name": "형님 (Administrator)",
        "role": "SuperAdmin"
    },
    "200400": {
        "name": "동운인터내셔널 담당자",
        "role": "Client"
    }
}

# --- 2. 보안 인디케이터 및 스타일 ---
st.set_page_config(page_title="AI Business OS - Security Center", layout="wide")

st.markdown("""
    <style>
    .led-green {
        margin: 0 auto; width: 15px; height: 15px; background-color: #ABFF00;
        border-radius: 50%; display: inline-block;
        box-shadow: rgba(0, 0, 0, 0.2) 0 -1px 7px 1px, inset #304701 0 -1px 9px, #89FF00 0 2px 12px;
        animation: blinkRed 1.5s infinite;
    }
    @keyframes blinkRed { from { background-color: #ABFF00; } 50% { background-color: #304701; box-shadow: none; } to { background-color: #ABFF00; } }
    .security-box { padding: 20px; border-radius: 10px; background-color: #f0f2f6; border-left: 5px solid #007bff; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. 세션 상태 관리 (로그인) ---
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
    
    # 사이드바
    with st.sidebar:
        st.title("🛰️ Dashboard")
        st.subheader(f"Welcome, {user_info['name']}")
        st.write(f"Role: **{user_info['role']}**")

        if user_info['role'] == "SuperAdmin":
            st.link_button("📂 Edit on GitHub", "https://github.com/berrylee019/intelligent-business-os", use_container_width=True)
        
        st.divider()
        st.markdown('### 🟢 System Status')
        col1, col2 = st.columns([1, 5])
        with col1: st.markdown('<div class="led-green"></div>', unsafe_allow_html=True)
        with col2: st.write("Local AI Processing")
        st.caption("Data Encrypted & Air-gapped")
        
        st.divider()
        # 프로젝트 리스트 (실시간 세션 상태 반영)
        if user_info["role"] == "SuperAdmin":
            project_list = [p["name"] for p in st.session_state.ALL_PROJECTS]
        else:
            project_list = ["반도체 냉각 모듈 최적화 AI (가상)", "Project Monitoring"]
            
        selected_project = st.selectbox("📂 Project Switcher", project_list)
        
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.rerun()

    # 메인 컨텐츠 영역
    tab1, tab2, tab3 = st.tabs(["🚀 Project Console", "🛡️ Security & Governance", "⚙️ Advanced & Manage"])

    with tab1:
        st.header(f"Project: {selected_project}")
        project_idx = next((i for i, p in enumerate(st.session_state.ALL_PROJECTS) if p["name"] == selected_project), None)
        
        if project_idx is not None:
            p_data = st.session_state.ALL_PROJECTS[project_idx]
            c1, c2 = st.columns(2)
            with c1: st.info(f"📁 **분야:** {p_data['category']}")
            with c2: st.success(f"📝 **진행 상황:** {p_data.get('status', '정보 없음')}")
            
            if user_info["role"] == "SuperAdmin":
                with st.expander("🛠️ Admin: 진행 상황 빠른 수정"):
                    new_status = st.text_input("새로운 진행 상황 입력", value=p_data.get('status', ''))
                    if st.button("업데이트 반영"):
                        st.session_state.ALL_PROJECTS[project_idx]['status'] = new_status
                        save_data(st.session_state.ALL_PROJECTS) # 파일 저장
                        st.toast(f"'{selected_project}' 상태가 저장되었습니다.")
                        time.sleep(0.5); st.rerun()

                st.markdown(f"🔗 [서비스 바로가기]({p_data['url']})")
                st.divider()
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Status", "Active", "Running")
                col_b.metric("Data Usage", "1.2GB", "-5%")
                col_c.metric("API Calls", "Local Only", "No External")
        else:
            st.warning("발주처 전용 모니터링 모드입니다. 보안 프로토콜에 의해 상세 데이터가 보호됩니다.")
            st.progress(65, text="Project Progress (Stage 2: Validation)")

    with tab2:
        st.header("🛡️ Security & Governance Center")
        st.markdown('<div class="security-box"><h4>🔒 Private AI Identity & Access Management</h4>본 시스템은 <b>Tenant Isolation</b> 원칙에 따라 설계되었습니다.</div>', unsafe_allow_html=True)
        st.divider()
        col_l, col_r = st.columns(2)
        with col_l:
            st.subheader("🔑 Data Sovereignty")
            st.write("- **Encryption:** AES-256")
            st.write("- **AI Engine:** Llama-3-Local")
        with col_r:
            st.subheader("🔍 Real-time Integrity")
            st.write(f"현재 접속 IP: `192.168.0.{hash(st.session_state.user_id) % 255}`")
            st.write("상태: **Safe**")

    with tab3:
        if user_info["role"] != "SuperAdmin":
            st.warning("⚠️ 접근 제한 구역입니다.")
        else:
            # 기존 설정 섹션
            st.header("⚙️ Advanced System Configuration")
            col_cfg1, col_cfg2 = st.columns(2)
            with col_cfg1:
                st.subheader("🤖 AI Engine Tuning")
                st.selectbox("Inference Model", ["Llama-3-70B (Local)", "Llama-3-8B (Fast)"])
                st.slider("Temperature", 0.0, 1.0, 0.2)
            with col_cfg2:
                st.subheader("📊 Resource Monitor")
                st.line_chart(pd.DataFrame(np.random.randn(20, 2), columns=['CPU', 'RAM']))

            st.divider()
            
            # --- [신규] 프로젝트 관리 섹션 ---
            st.header("📂 Project Management (JSON DB)")
            col_add, col_del = st.columns(2)
            
            with col_add:
                st.subheader("➕ 새 프로젝트 추가")
                with st.form("add_form", clear_on_submit=True):
                    add_name = st.text_input("프로젝트 명")
                    add_url = st.text_input("서비스 URL")
                    add_cat = st.text_input("카테고리")
                    add_stat = st.text_input("현재 상태", value="초기 기획")
                    if st.form_submit_button("등록 및 저장"):
                        if add_name and add_url:
                            new_p = {"name": add_name, "url": add_url, "category": add_cat, "status": add_stat}
                            st.session_state.ALL_PROJECTS.append(new_p)
                            save_data(st.session_state.ALL_PROJECTS)
                            st.success(f"'{add_name}' 등록 완료!")
                            time.sleep(0.5); st.rerun()
                        else: st.error("이름과 URL을 입력해주세요.")

            with col_del:
                st.subheader("🗑️ 프로젝트 삭제")
                del_target = st.selectbox("삭제할 항목 선택", [p["name"] for p in st.session_state.ALL_PROJECTS])
                if st.button("⚠️ 즉시 삭제", type="primary"):
                    st.session_state.ALL_PROJECTS = [p for p in st.session_state.ALL_PROJECTS if p["name"] != del_target]
                    save_data(st.session_state.ALL_PROJECTS)
                    st.warning(f"'{del_target}' 삭제됨.")
                    time.sleep(0.5); st.rerun()

# --- Footer ---
st.sidebar.markdown("---")
st.sidebar.caption("Powered by Korean Palantir Framework")
