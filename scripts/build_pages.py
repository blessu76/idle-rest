#!/usr/bin/env python3
"""Build the idle.ipe.rest trust pages (About / Contact / Privacy Policy, EN + KO).

Dependency-free (Python 3.8+ stdlib). Reuses the page chrome of build_journal.py,
so the header, footer and asset version stay identical across the site.

Writes  about/index.html    contact/index.html    privacy/index.html      (English)
        ko/about/index.html ko/contact/index.html ko/privacy/index.html   (Korean)

The pages are generated: edit the PAGES text below, then run
    python3 scripts/build_pages.py
Running it twice produces identical files (idempotent).
"""
import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import build_journal as bj  # noqa: E402

SITE = bj.SITE
OPERATOR = "Davy Kim (ipe Studio)"
EMAIL = "ipe.haven@gmail.com"
EFFECTIVE = "2026-10-20"
REPLY_DAYS = 10
SLUGS = ("about", "contact", "privacy")

SOCIAL = (
    ("YouTube", "https://www.youtube.com/@ipe-rest"),
    ("Instagram", "https://www.instagram.com/ipe.rest"),
    ("SoundCloud", "https://soundcloud.com/ipe-rest"),
)
SOCIAL_LI = "\n".join('<li><a href="%s" rel="noopener">%s</a></li>' % (u, n) for n, u in SOCIAL)

# ------------------------------------------------------------------ English
EN = {
    "about": {
        "title": "About idle() — the music of ipe()",
        "desc": "Who runs idle.ipe.rest and how the music is made: AI lo-fi and healing music for tired developers, made by Davy Kim (ipe Studio).",
        "h1": "About idle()",
        "sub": "Quiet lo-fi for the moment your work pauses.",
        "body": f"""
<p>idle() is the music of ipe() — calm lo-fi, ambient and healing tracks for tired developers and late-night focus. This site, <strong>idle.ipe.rest</strong>, is where the music lives: you can browse the albums and singles, read the journal, and open every track on YouTube in English or Korean.</p>

<h2>Who runs this site</h2>
<p>idle.ipe.rest is operated by <strong>{OPERATOR}</strong>, an individual developer. ipe() is short for “idle process” — the state a computer enters when it has no work to do and simply rests. It is a small, independent studio making quiet, developer-minded things, and idle() is its music.</p>
<p>You can reach the operator at <a href="mailto:{EMAIL}">{EMAIL}</a> (see <a href="/contact/">Contact</a>).</p>

<h2>How the music is made</h2>
<p>We do not hide how the music is made. The music is produced with AI (Suno). Lyrics are AI-drafted and reviewed by a person. Since the <em>dear(you);</em> album, every track closes with a quiet spoken signature — “ipe. be still”.</p>
<p>Our first album, <em>dear(you); vol.1</em>, is ten letters to the you who made it through another hard day. Two singles, “good morning, world” and “still compiling”, sit beside it.</p>

<h2>What you will find here</h2>
<ul>
<li>The album and singles, with a small player that opens each track on YouTube (English or Korean version).</li>
<li>A <a href="/journal/">journal</a> with notes from behind the music.</li>
<li>Links to our channels: {", ".join('<a href="%s" rel="noopener">%s</a>' % (u, n) for n, u in SOCIAL)}.</li>
</ul>

<h2>Free to listen, supported by ads</h2>
<p>Everything on this site is free to listen to. To help cover running costs, the site may show advertising, always labelled “Advertisement” and kept apart from the content. How ads and analytics work is explained in the <a href="/privacy/">Privacy Policy</a>.</p>

<h2>Corrections and feedback</h2>
<p>If you find a mistake, a broken link, or something that does not feel right, please write to <a href="mailto:{EMAIL}">{EMAIL}</a>. We read every message.</p>
""",
    },
    "contact": {
        "title": "Contact — idle() · the music of ipe()",
        "desc": f"How to reach the operator of idle.ipe.rest: email {EMAIL}. We reply within {REPLY_DAYS} days.",
        "h1": "Contact",
        "sub": f"We reply within {REPLY_DAYS} days.",
        "body": f"""
<div class="contact-card">
<p><strong>Operator</strong><br>{OPERATOR}</p>
<p><strong>Email</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><strong>Reply time</strong><br>We aim to reply within {REPLY_DAYS} days. This is a one-person studio, so thank you for your patience.</p>
</div>

<h2>What you can write to us about</h2>
<ul>
<li><strong>General questions and feedback</strong> about the music or the site.</li>
<li><strong>Privacy requests</strong> — to see, correct or delete personal information, or to ask a question about the <a href="/privacy/">Privacy Policy</a>.</li>
<li><strong>Copyright or content concerns</strong> — tell us which page or track and what the concern is.</li>
<li><strong>Collaboration or press</strong> enquiries.</li>
<li><strong>Problems with the site or an advertisement</strong> — please include the page address and, if you can, a short description or screenshot.</li>
</ul>

<h2>Elsewhere</h2>
<ul>
{SOCIAL_LI}
</ul>
<p>For anything that involves personal information, please use email rather than social media messages.</p>
""",
    },
    "privacy": {
        "title": "Privacy Policy — idle() · the music of ipe()",
        "desc": "How idle.ipe.rest handles your information: analytics, cookies, local storage, and Google AdSense advertising.",
        "h1": "Privacy Policy",
        "sub": f"Effective date: {EFFECTIVE}",
        "body": f"""
<p>This policy explains what information idle.ipe.rest (“the Site”) handles when you visit, and the choices you have. The Site is operated by <strong>{OPERATOR}</strong> (“we”, “us”), an individual developer. <strong>Effective date: {EFFECTIVE}.</strong></p>
<p>In short: there are no accounts, no sign-up forms and no comments on this Site, and we do not ask you for personal information. We do use analytics, and the Site may show ads from Google AdSense, and both can involve cookies — explained below.</p>

<h2>1. Information we collect</h2>
<ul>
<li><strong>Information you send us.</strong> If you email us, we receive your email address and what you write, and use it only to reply.</li>
<li><strong>Usage data (automatic).</strong> Through the analytics tools below we receive technical and usage information such as the pages you view, the track you choose, approximate location (city or country level), device and browser type, language and referring page. We do not use this to identify you personally.</li>
<li><strong>Server logs.</strong> The Site is hosted on GitHub Pages. The host may process technical request data such as your IP address as part of delivering the pages.</li>
</ul>

<h2>2. Analytics</h2>
<div class="table-wrap"><table class="doc-table">
<thead><tr><th>Tool</th><th>Purpose</th><th>How it works</th></tr></thead>
<tbody>
<tr><td>Google Analytics 4 (Google)</td><td>Understand which pages and tracks are used</td><td>Uses cookies or similar identifiers and sends usage data to Google. When you press play, a short redirect page records which track you chose (an anonymous event) before opening YouTube.</td></tr>
<tr><td>Cloudflare Web Analytics (Cloudflare)</td><td>Page-view and performance statistics</td><td>Privacy-first and cookieless; it does not track or profile individual visitors.</td></tr>
</tbody></table></div>
<p>You can opt out of Google Analytics with the <a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google Analytics opt-out browser add-on</a>. Learn how Google handles this data at <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">How Google uses information from sites or apps that use our services</a>.</p>

<h2>3. Advertising (Google AdSense)</h2>
<p>The Site may display advertising served by Google AdSense. Third-party vendors, including Google, use cookies to serve ads based on a user’s prior visits to this website or other websites. Google’s use of advertising cookies enables it and its partners to serve ads to users based on their visit to this Site and/or other sites on the Internet.</p>
<p>You can opt out of personalized advertising by visiting <a href="https://adssettings.google.com" rel="noopener">Google Ads Settings</a>. Alternatively, you can opt out of a third-party vendor’s use of cookies for personalized advertising by visiting <a href="https://www.aboutads.info" rel="noopener">www.aboutads.info</a>.</p>
<p>We do not control the cookies set by Google or other ad partners, and we do not receive your personal information from them.</p>

<h2>4. Cookies and local storage</h2>
<ul>
<li><strong>Cookies</strong> may be set by Google Analytics and by Google and its advertising partners, as described above. You can block or delete cookies in your browser settings; the Site still works without them.</li>
<li><strong>Local storage.</strong> The Site saves two small preferences in your browser’s localStorage: your theme (light or dark) and your language. They stay on your device, are not sent to us, and you can clear them at any time in your browser.</li>
</ul>

<h2>5. How we use and share information</h2>
<p>We use the information above to run and improve the Site, understand how it is used, show advertising that supports it, and reply to you. We do not sell your personal information. We share data only with the service providers named in this policy (Google, Cloudflare and the hosting provider), and where the law requires.</p>

<h2>6. Retention</h2>
<p>We keep emails only as long as needed to reply and follow up, and delete them on request. Analytics data is handled in aggregate and is kept by the providers under their own retention settings.</p>

<h2>7. International transfers</h2>
<p>Google, Cloudflare and GitHub operate globally, so information may be processed in countries other than your own, including the United States.</p>

<h2>8. Third-party links</h2>
<p>The Site links to YouTube, Instagram, SoundCloud and other sites. They have their own privacy practices, which we do not control; please read their policies.</p>

<h2>9. Your choices and rights</h2>
<p>You may ask us to access, correct or delete the personal information we hold about you (for example, an email you sent), or to restrict how it is used. Email <a href="mailto:{EMAIL}">{EMAIL}</a> and we will reply within {REPLY_DAYS} days. Because we do not keep accounts or profiles, in most cases there will be little or nothing beyond your email to act on. You can also use the opt-out tools in sections 2 and 3, and your browser’s cookie controls.</p>
<p>If you are in Korea, you may also contact the Personal Information Dispute Mediation Committee (1833-6972, kopico.go.kr) or the Personal Information Infringement Report Center (118, privacy.kisa.or.kr). If you are in the EEA or the UK, you may contact your local data protection authority.</p>

<h2>10. Children</h2>
<p>The Site is not directed to children under 14, and we do not knowingly collect personal information from them.</p>

<h2>11. Changes to this policy</h2>
<p>We may update this policy. When we do, we will change the effective date above. Material changes will be noted on this page.</p>

<h2>12. Contact</h2>
<p>{OPERATOR} — <a href="mailto:{EMAIL}">{EMAIL}</a>. The operator is also responsible for handling personal information and complaints.</p>
""",
    },
}

# ------------------------------------------------------------------ Korean
KO = {
    "about": {
        "title": "소개 — idle() · the music of ipe()",
        "desc": "idle.ipe.rest 운영 주체와 음악을 만드는 방식을 소개합니다. 지친 개발자를 위한 AI 로파이·힐링 음악, Davy Kim (ipe Studio).",
        "h1": "idle() 소개",
        "sub": "일이 잠시 멈추는 순간을 위한 조용한 로파이.",
        "body": f"""
<p>idle()는 ipe()의 음악입니다. 지친 개발자와 늦은 밤의 집중을 위한 잔잔한 로파이·앰비언트·힐링 트랙을 만듭니다. 이 사이트 <strong>idle.ipe.rest</strong>는 그 음악이 머무는 곳으로, 앨범과 싱글을 둘러보고 저널을 읽고, 모든 곡을 영어·한국어 두 버전으로 YouTube에서 들을 수 있습니다.</p>

<h2>운영 주체</h2>
<p>idle.ipe.rest는 개인 개발자 <strong>Davy Kim (ipe Studio)</strong>이 운영합니다. ipe()는 「idle process」의 줄임말로, 컴퓨터가 할 일이 없어 가만히 쉬는 상태를 뜻합니다. 조용하고 개발자다운 것들을 만드는 작은 독립 스튜디오이고, idle()는 그 음악입니다.</p>
<p>운영자에게는 <a href="mailto:{EMAIL}">{EMAIL}</a>로 연락하실 수 있습니다(<a href="/ko/contact/">문의</a> 참고).</p>

<h2>음악을 만드는 방식</h2>
<p>음악을 어떻게 만드는지 숨기지 않습니다. 음악은 AI(Suno)로 만들고, 가사는 AI 초안을 사람이 검토합니다. <em>dear(you);</em> 앨범부터 모든 곡은 「ipe. be still」이라는 조용한 속삭임으로 끝납니다.</p>
<p>첫 앨범 <em>dear(you); vol.1</em>은 힘든 하루를 또 넘긴 당신에게 보내는 열 통의 편지입니다. 싱글 「good morning, world」와 「still compiling」이 함께 있습니다.</p>

<h2>이 사이트에서 볼 수 있는 것</h2>
<ul>
<li>앨범과 싱글, 그리고 각 곡을 YouTube(영어·한국어 버전)로 여는 작은 플레이어.</li>
<li>음악 뒷이야기를 담은 <a href="/journal/">저널</a>.</li>
<li>채널 링크: {", ".join('<a href="%s" rel="noopener">%s</a>' % (u, n) for n, u in SOCIAL)}.</li>
</ul>

<h2>무료로 듣고, 광고로 운영합니다</h2>
<p>이 사이트의 모든 음악은 무료로 들을 수 있습니다. 운영비에 보탬이 되도록 광고가 표시될 수 있으며, 광고는 항상 「광고」로 표시하고 콘텐츠와 구분합니다. 광고와 분석 도구가 어떻게 동작하는지는 <a href="/ko/privacy/">개인정보처리방침</a>에 있습니다.</p>

<h2>정정과 의견</h2>
<p>오류나 깨진 링크, 어색한 부분을 발견하시면 <a href="mailto:{EMAIL}">{EMAIL}</a>로 알려 주세요. 모든 메시지를 읽습니다.</p>
""",
    },
    "contact": {
        "title": "문의 — idle() · the music of ipe()",
        "desc": f"idle.ipe.rest 운영자 연락처: 이메일 {EMAIL}. {REPLY_DAYS}일 이내에 답장드립니다.",
        "h1": "문의",
        "sub": f"{REPLY_DAYS}일 이내에 답장드립니다.",
        "body": f"""
<div class="contact-card">
<p><strong>운영 주체</strong><br>{OPERATOR}</p>
<p><strong>이메일</strong><br><a href="mailto:{EMAIL}">{EMAIL}</a></p>
<p><strong>답장 시간</strong><br>{REPLY_DAYS}일 이내에 답장드리는 것을 목표로 합니다. 1인 스튜디오라서 조금 늦을 수 있으니 양해 부탁드립니다.</p>
</div>

<h2>이런 내용을 보내 주세요</h2>
<ul>
<li><strong>일반 문의·의견</strong> — 음악이나 사이트에 관한 이야기.</li>
<li><strong>개인정보 요청</strong> — 개인정보 열람·정정·삭제, 또는 <a href="/ko/privacy/">개인정보처리방침</a>에 관한 질문.</li>
<li><strong>저작권·콘텐츠 관련 문의</strong> — 어느 페이지나 곡인지, 어떤 내용인지 알려 주세요.</li>
<li><strong>협업·취재</strong> 문의.</li>
<li><strong>사이트 또는 광고 문제</strong> — 페이지 주소와 가능하면 간단한 설명이나 스크린샷을 함께 보내 주세요.</li>
</ul>

<h2>다른 채널</h2>
<ul>
{SOCIAL_LI}
</ul>
<p>개인정보와 관련된 내용은 SNS 메시지가 아닌 이메일로 보내 주세요.</p>
""",
    },
    "privacy": {
        "title": "개인정보처리방침 — idle() · the music of ipe()",
        "desc": "idle.ipe.rest가 방문자 정보를 어떻게 다루는지 안내합니다: 분석 도구, 쿠키, 로컬 저장소, Google AdSense 광고.",
        "h1": "개인정보처리방침",
        "sub": f"시행일: {EFFECTIVE}",
        "body": f"""
<p>이 방침은 방문자가 idle.ipe.rest(이하 「사이트」)를 이용할 때 어떤 정보가 처리되는지, 그리고 선택할 수 있는 방법을 안내합니다. 사이트는 개인 개발자 <strong>Davy Kim (ipe Studio)</strong>(이하 「운영자」)이 운영합니다. <strong>시행일: {EFFECTIVE}.</strong></p>
<p>요약하면, 이 사이트에는 회원가입·가입 양식·댓글이 없고 개인정보를 직접 요청하지 않습니다. 다만 분석 도구를 사용하고 Google AdSense 광고가 표시될 수 있으며, 둘 다 쿠키를 사용할 수 있습니다. 자세한 내용은 아래와 같습니다.</p>

<h2>1. 수집하는 정보</h2>
<ul>
<li><strong>이용자가 보내 주시는 정보.</strong> 이메일로 문의하시면 이메일 주소와 작성하신 내용을 받으며, 답장하는 용도로만 사용합니다.</li>
<li><strong>자동으로 수집되는 이용 정보.</strong> 아래 분석 도구를 통해 조회한 페이지, 선택한 곡, 대략적인 위치(도시·국가 수준), 기기·브라우저 종류, 언어, 유입 페이지 등 기술·이용 정보를 받습니다. 이 정보로 개인을 식별하지 않습니다.</li>
<li><strong>서버 기록.</strong> 사이트는 GitHub Pages에서 제공됩니다. 호스팅 사업자는 페이지 전달 과정에서 IP 주소 등 기술적 요청 정보를 처리할 수 있습니다.</li>
</ul>

<h2>2. 분석 도구</h2>
<div class="table-wrap"><table class="doc-table">
<thead><tr><th>도구</th><th>목적</th><th>동작 방식</th></tr></thead>
<tbody>
<tr><td>Google Analytics 4 (Google)</td><td>어떤 페이지와 곡이 이용되는지 파악</td><td>쿠키 또는 유사한 식별자를 사용하고 이용 데이터를 Google로 보냅니다. 재생 버튼을 누르면 YouTube로 이동하기 전에 짧은 연결 페이지가 선택한 곡을 익명 이벤트로 기록합니다.</td></tr>
<tr><td>Cloudflare Web Analytics (Cloudflare)</td><td>페이지 조회·성능 통계</td><td>개인정보 보호 중심의 쿠키 없는 방식으로, 개별 방문자를 추적하거나 프로파일링하지 않습니다.</td></tr>
</tbody></table></div>
<p><a href="https://tools.google.com/dlpage/gaoptout" rel="noopener">Google Analytics 차단 브라우저 부가기능</a>으로 Google Analytics 수집을 거부할 수 있습니다. Google의 데이터 처리 방식은 <a href="https://policies.google.com/technologies/partner-sites" rel="noopener">Google이 파트너 사이트나 앱의 정보를 사용하는 방법</a>에서 확인하실 수 있습니다.</p>

<h2>3. 광고 (Google AdSense)</h2>
<p>사이트에는 Google AdSense가 제공하는 광고가 표시될 수 있습니다. Google을 포함한 제3자 공급업체는 쿠키를 사용하여 사용자가 이 웹사이트 또는 다른 웹사이트를 이전에 방문한 기록을 바탕으로 광고를 게재합니다. Google은 광고 쿠키를 사용하여 사용자가 이 사이트 및/또는 인터넷상의 다른 사이트를 방문한 기록을 바탕으로 Google과 파트너가 광고를 게재할 수 있습니다.</p>
<p>맞춤 광고는 <a href="https://adssettings.google.com" rel="noopener">Google 광고 설정</a>에서 끌 수 있습니다. 또는 <a href="https://www.aboutads.info" rel="noopener">www.aboutads.info</a>를 방문하여 제3자 공급업체의 맞춤 광고용 쿠키 사용을 거부할 수 있습니다.</p>
<p>운영자는 Google 및 광고 파트너가 설정하는 쿠키를 통제하지 않으며, 그들로부터 이용자의 개인정보를 전달받지 않습니다.</p>

<h2>4. 쿠키와 로컬 저장소</h2>
<ul>
<li><strong>쿠키</strong>는 위에서 설명한 대로 Google Analytics, 그리고 Google과 광고 파트너가 설정할 수 있습니다. 브라우저 설정에서 쿠키를 차단하거나 삭제할 수 있으며, 쿠키가 없어도 사이트는 동작합니다.</li>
<li><strong>로컬 저장소.</strong> 사이트는 브라우저의 localStorage에 테마(밝은/어두운)와 언어, 두 가지 설정만 저장합니다. 이 값은 이용자의 기기에만 남고 운영자에게 전송되지 않으며, 브라우저에서 언제든 지울 수 있습니다.</li>
</ul>

<h2>5. 정보의 이용과 제공</h2>
<p>위 정보는 사이트를 운영·개선하고, 이용 현황을 파악하고, 사이트를 지원하는 광고를 표시하고, 문의에 답장하는 데 사용합니다. 개인정보를 판매하지 않습니다. 이 방침에 적은 서비스 제공업체(Google, Cloudflare, 호스팅 사업자)에게만, 그리고 법령이 요구하는 경우에만 정보가 제공됩니다.</p>

<h2>6. 보유 기간</h2>
<p>이메일은 답장과 후속 대응에 필요한 기간 동안만 보관하며, 요청하시면 삭제합니다. 분석 데이터는 통계 형태로 다루며, 각 제공업체의 보유 기간 설정에 따라 보관됩니다.</p>

<h2>7. 국외 이전</h2>
<p>Google, Cloudflare, GitHub는 전 세계에서 서비스를 운영하므로 정보가 이용자의 국가가 아닌 미국 등 다른 국가에서 처리될 수 있습니다.</p>

<h2>8. 외부 링크</h2>
<p>사이트는 YouTube, Instagram, SoundCloud 등 외부 사이트로 연결됩니다. 해당 사이트의 개인정보 처리는 운영자가 통제할 수 없으니 각 방침을 확인해 주세요.</p>

<h2>9. 이용자의 선택과 권리</h2>
<p>보유 중인 본인의 개인정보(예: 보내 주신 이메일)에 대해 열람·정정·삭제·처리정지를 요청하실 수 있습니다. <a href="mailto:{EMAIL}">{EMAIL}</a>로 요청하시면 {REPLY_DAYS}일 이내에 답장드립니다. 계정이나 프로필을 보관하지 않으므로 대부분의 경우 이메일 외에 처리할 정보가 거의 없습니다. 위 2·3항의 거부 방법과 브라우저의 쿠키 설정도 사용하실 수 있습니다.</p>
<p>개인정보 침해에 대한 구제가 필요하시면 개인정보분쟁조정위원회(1833-6972, kopico.go.kr) 또는 개인정보침해신고센터(118, privacy.kisa.or.kr)에 문의하실 수 있습니다.</p>

<h2>10. 아동</h2>
<p>사이트는 만 14세 미만 아동을 대상으로 하지 않으며, 아동의 개인정보를 알면서 수집하지 않습니다.</p>

<h2>11. 방침의 변경</h2>
<p>이 방침은 바뀔 수 있으며, 바뀌면 위의 시행일을 고칩니다. 중요한 변경은 이 페이지에 알립니다.</p>

<h2>12. 문의 및 개인정보 보호책임자</h2>
<p>Davy Kim (ipe Studio) — <a href="mailto:{EMAIL}">{EMAIL}</a>. 운영자가 개인정보 처리와 불만 처리를 직접 맡습니다.</p>
""",
    },
}

LANGS = {"en": EN, "ko": KO}
PREFIX = {"en": "", "ko": "/ko"}


def url_path(lang, slug):
    return "%s/%s/" % (PREFIX[lang], slug)


def render(lang, slug):
    pg = LANGS[lang][slug]
    other = "ko" if lang == "en" else "en"
    canonical = SITE + url_path(lang, slug)
    alts = (
        '<link rel="alternate" hreflang="en" href="%s%s">\n' % (SITE, url_path("en", slug))
        + '<link rel="alternate" hreflang="ko" href="%s%s">\n' % (SITE, url_path("ko", slug))
        + '<link rel="alternate" hreflang="x-default" href="%s%s">\n' % (SITE, url_path("en", slug))
    )
    ldobj = {
        "@context": "https://schema.org",
        "@type": "AboutPage" if slug == "about" else ("ContactPage" if slug == "contact" else "WebPage"),
        "name": pg["title"],
        "url": canonical,
        "inLanguage": lang,
        "isPartOf": {"@type": "WebSite", "name": "idle() — the music of ipe()", "url": SITE + "/"},
        "publisher": {"@type": "Organization", "name": "ipe()", "url": "https://ipe.rest/"},
    }
    extra = alts + bj.ld(ldobj)
    page = bj.head(pg["title"], pg["desc"], canonical, lang, False, extra=extra,
                   hint="edit scripts/build_pages.py and rebuild")
    page += bj.header(lang, current=slug, alt=(url_path(other, slug), other))
    page += '<main id="main" class="shell">\n<div class="doc">\n'
    page += '<div class="page-head">\n  <h1>%s</h1>\n  <p>%s</p>\n</div>\n' % (bj.esc(pg["h1"]), bj.esc(pg["sub"]))
    page += '<div class="prose">%s</div>\n</div>\n</main>\n' % pg["body"].rstrip()
    page += bj.footer(lang)
    return page


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--root", default=str(Path(__file__).resolve().parent.parent), help="site root (default: this repo)")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    # ASSET_V / ads switch must match index.html (same rule as build_journal.py)
    m = re.search(r'<html[^>]*\sdata-ads="(on|off)"', (root / "index.html").read_text(encoding="utf-8"))
    bj.ADS_ATTR = m.group(1) if m else "off"
    n = 0
    for lang in LANGS:
        for slug in SLUGS:
            d = root / PREFIX[lang].strip("/") / slug
            d.mkdir(parents=True, exist_ok=True)
            (d / "index.html").write_text(render(lang, slug), encoding="utf-8")
            n += 1
    print("pages: built %d page(s)" % n)
    return 0


if __name__ == "__main__":
    sys.exit(main())
