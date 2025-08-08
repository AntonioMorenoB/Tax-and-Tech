"use client";
import useSWR from "swr";
import { useState } from "react";
const fetcher = (u:string)=>fetch(u).then(r=>r.json());
export default function Page(){
  const { data: health } = useSWR(`/api/health`, fetcher);
  const { data: news } = useSWR(`/api/news`, fetcher);
  const [q,setQ]=useState(""); const [res,setRes]=useState<any[]>([]);
  async function search(){
    const r = await fetch(`/api/legal/search?q=${encodeURIComponent(q)}`);
    const j = await r.json(); setRes(j.results||[]);
  }
  return (
    <main style={{padding:24, maxWidth:1100, margin:"0 auto"}}>
      <h1 style={{fontSize:28, marginBottom:6}}>Tax and Technology AM</h1>
      <div className="small">API: {health?.status||"..."}</div>
      <div className="grid" style={{marginTop:16}}>
        <section className="card">
          <h2>Buscador Legal (demo)</h2>
          <div style={{display:"flex",gap:8, marginTop:8}}>
            <input placeholder="Ej: CFDI 4.0 requisitos" value={q} onChange={e=>setQ(e.target.value)} style={{flex:1}}/>
            <button onClick={search}>Buscar</button>
          </div>
          <div style={{marginTop:12}}>
            {res.map((r,i)=>(
              <div key={i} style={{marginBottom:12}}>
                <div className="mono small">#{r.id} · {new Date(r.updated_at).toLocaleString()}</div>
                <div style={{fontWeight:700}}>{r.title}</div>
                <div className="small">{r.snippet}...</div>
              </div>
            ))}
            {res.length===0 && <div className="small">Sin resultados aún.</div>}
          </div>
        </section>
        <section className="card">
          <h2>Noticias</h2>
          <div className="small">Prueba de feed (SAT/Banxico).</div>
          <div style={{marginTop:8}}>
            {!news && <div className="small">Cargando...</div>}
            {news && news.map((n:any,i:number)=>(
              <a key={i} href={n.url} target="_blank">
                <div style={{marginBottom:12}}>
                  <div style={{fontWeight:700}}>{n.title}</div>
                  <div className="small">{n.source} · {new Date(n.published_at).toLocaleDateString()}</div>
                  <div className="small">{n.summary}</div>
                </div>
              </a>
            ))}
          </div>
        </section>
        <section className="card">
          <h2>Subir CFDI</h2>
          <form action={`/api/cfdi/upload`} method="post" encType="multipart/form-data" target="_blank">
            <input type="file" name="xml" accept=".xml" />
            <button type="submit">Procesar</button>
          </form>
          <p className="small">Extrae RFCs/total (demo).</p>
        </section>
      </div>
    </main>
  );
}