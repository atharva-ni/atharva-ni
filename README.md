<img src="./assets/banner.svg" alt="Atharva Nighot. Models, web apps, and the hardware they run on." width="100%">

<p>
  <a href="https://www.linkedin.com/in/atharva-nighot-223a16212"><img src="https://skillicons.dev/icons?i=linkedin" height="34" alt="LinkedIn"></a>&nbsp;
  <a href="mailto:atharva.nighot0030@gmail.com"><img src="https://skillicons.dev/icons?i=gmail" height="34" alt="Email"></a>
</p>

I'm Atharva, a developer from Pune who likes owning a product end to end: the model, the app around it, and sometimes the device it runs on. I studied Artificial Intelligence & Data Science at MMCOE, Pune (B.E., 2023–2026, CGPA 9.5), and I build production web apps for real businesses, mostly with Next.js, TypeScript and Supabase.

Right now I'm working on **Survey Excluder**, a classifier that finds survey papers in a researcher's publication list so citation metrics can be read without them. It's the code and data behind a paper I wrote with Nima Afraz.

## Selected work

<table>
<tr>
<td width="50%" valign="top">
<p><b><a href="https://github.com/atharva-ni/SurveyExcluderModel">Survey Excluder</a></b><br>
Detects survey and review papers from bibliographic metadata and recalculates h-index, i10-index and citations without them. Fine-tuned DistilBERT feeds a learned hybrid classifier: 93.6% accuracy and 93.2% F1 on 1,925 held-out papers. Comes with a <a href="https://github.com/atharva-ni/SurvayExtruderUI">web app</a> for uploading a publication list.</p>
<p><code>PyTorch</code> <code>DistilBERT</code> <code>scikit-learn</code> <code>FastAPI</code> <code>React</code> <code>TypeScript</code> <code>OpenAlex API</code></p>
</td>
<td width="50%" valign="top">
<p><b><a href="https://github.com/atharva-ni/Restro">AI table-ordering kiosk</a></b><br>
A self-ordering kiosk that runs on a Raspberry Pi 4 touchscreen at each restaurant table. Guests tap or talk: speech streams to Deepgram, Groq's LLaMA 3.1 turns it into an order, and ElevenLabs answers back. The kitchen display and admin panel update live.</p>
<p><code>Next.js 14</code> <code>TypeScript</code> <code>Supabase Realtime</code> <code>Prisma</code> <code>Zustand</code> <code>Deepgram</code> <code>Groq</code> <code>ElevenLabs</code></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<p><b><a href="https://github.com/atharva-ni/Restro-Saas">RestaurantOS</a></b><br>
Multi-tenant SaaS for restaurants: menu and reservation management in a Next.js dashboard, plus a WhatsApp bot on the Meta Cloud API that takes bookings through a conversational state machine.</p>
<p><code>Next.js 14</code> <code>Express</code> <code>Supabase</code> <code>PostgreSQL</code> <code>WhatsApp Cloud API</code> <code>JWT</code></p>
</td>
<td width="50%" valign="top">
<p><b><a href="https://github.com/atharva-ni/Medsys">Medsys</a></b><br>
Ordering and fulfilment platform for a medicine distributor. Customers order through a WhatsApp button-and-list bot built in n8n, and orders land in a dashboard for the distributor's team.</p>
<p><code>Next.js</code> <code>TypeScript</code> <code>Supabase</code> <code>shadcn/ui</code> <code>n8n</code> <code>WhatsApp</code></p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<p><b><a href="https://github.com/atharva-ni/Skilotech">Skillzy</a></b><br>
A learning platform with a drag-to-reorder course builder for instructors, in-browser coding labs on the Monaco editor for students, Razorpay checkout in INR, and Redis caching on curriculum queries.</p>
<p><code>Next.js</code> <code>TypeScript</code> <code>PostgreSQL</code> <code>Prisma</code> <code>Redis</code> <code>Clerk</code> <code>Razorpay</code></p>
</td>
<td width="50%" valign="top">
<p><b><a href="https://github.com/atharva-ni/zip">Libra</a></b><br>
An automated library. Students request books on the web, robots and smart bins handle issue and return, and NFC tags confirm every book that moves. A TF-IDF recommender suggests what to read next.</p>
<p><code>React</code> <code>Vite</code> <code>FastAPI</code> <code>Prisma</code> <code>scikit-learn</code> <code>NFC</code></p>
</td>
</tr>
</table>

Also built:

- [Real-time coding battles](https://github.com/atharva-ni/Game) over Socket.io, with every submission run in a Docker sandbox
- [ResumeRack](https://github.com/atharva-ni/ResumeRank), a fine-tuned BERT model that ranks resumes against a job description
- Business websites on Next.js 16 for [Vighnaharta Engineers](https://www.vighanahartaengineers.in) and [Aditya Electro Infra](https://github.com/atharva-ni/Adityaelectroinfra)
- An autonomous fire-detection robot (2022) with a 3D-printed chassis, MQ2 smoke sensors, an ESP32-CAM live feed and a SIM800L module that calls the fire department; shown at the state-level Dipex exhibition

## Experience

| Role | Where | When |
|---|---|---|
| Full Stack Development Intern | Vighnaharta Engineers, Pune | Jan – Apr 2025 |
| Java Development Intern | R3 Systems, Nashik | Jun – Aug 2022 |

At Vighnaharta I built and shipped the company's website and worked on its web apps from design to deployment. At R3 Systems I wrote backend features in Java and SQL.

## Tools I reach for

| Area | Tools |
|---|---|
| Languages | <img src="https://skillicons.dev/icons?i=ts,js,py,cpp,c,java&perline=8" height="40" alt="TypeScript, JavaScript, Python, C++, C, Java"> |
| Web | <img src="https://skillicons.dev/icons?i=nextjs,react,tailwind,vite,html,css&perline=8" height="40" alt="Next.js, React, Tailwind CSS, Vite, HTML, CSS"> |
| Backend and data | <img src="https://skillicons.dev/icons?i=nodejs,express,fastapi,flask,supabase,postgres,prisma,mongodb,mysql,redis,firebase&perline=11" height="40" alt="Node.js, Express, FastAPI, Flask, Supabase, PostgreSQL, Prisma, MongoDB, MySQL, Redis, Firebase"> |
| AI and ML | <img src="https://skillicons.dev/icons?i=pytorch,sklearn&perline=8" height="40" alt="PyTorch, scikit-learn"> &nbsp;plus Hugging Face Transformers, Groq, Deepgram |
| Hardware and ops | <img src="https://skillicons.dev/icons?i=raspberrypi,arduino,docker,linux,git,vercel&perline=8" height="40" alt="Raspberry Pi, Arduino, Docker, Linux, Git, Vercel"> |

## On GitHub

<p>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/atharva-ni/atharva-ni/main/profile/stats-dark.svg">
    <img src="https://raw.githubusercontent.com/atharva-ni/atharva-ni/main/profile/stats-light.svg" alt="Atharva's GitHub stats" height="165">
  </picture>
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/atharva-ni/atharva-ni/main/profile/top-langs-dark.svg">
    <img src="https://raw.githubusercontent.com/atharva-ni/atharva-ni/main/profile/top-langs-light.svg" alt="Most used languages" height="165">
  </picture>
</p>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/atharva-ni/atharva-ni/main/profile/snake-dark.svg">
  <img src="https://raw.githubusercontent.com/atharva-ni/atharva-ni/main/profile/snake-light.svg" alt="Contribution graph being eaten by a snake" width="100%">
</picture>

## Education and recognition

**B.E. in Artificial Intelligence & Data Science**, Marathwada Mitra Mandal's College of Engineering, Pune (2023–2026), CGPA 9.5<br>
**Diploma in Computer Technology**, K.K. Wagh Polytechnic, Nashik (2020–2023), 86.70%

<details>
<summary>Certifications and leadership</summary>
<br>

- Introduction to Cybersecurity, Cybersecurity Essentials, and Introduction to Packet Tracer (Cisco Networking Academy, 2024)
- SQL certification (HackerRank, 2024)
- Committee Head for ACTS 2022, running the event's activities and competitions end to end
- Fire Detection & Security Robot presented at Dipex 2022, a state-level student project exhibition

</details>

---

The quickest way to reach me is [LinkedIn](https://www.linkedin.com/in/atharva-nighot-223a16212) or [atharva.nighot0030@gmail.com](mailto:atharva.nighot0030@gmail.com). I'm always happy to talk about Next.js and Supabase architecture, fine-tuning small transformers, or getting a Raspberry Pi to behave in production.
