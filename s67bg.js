(function(){"use strict";var W=window,D=document,de=D.documentElement;if(W.__s67bg)return;W.__s67bg=1;
var q=null,mode="season";try{q=new URLSearchParams(location.search).get("s");if(q==="glass"||q==="season")localStorage.setItem("s67mode",q);mode=localStorage.getItem("s67mode")||"season"}catch(e){}
if(mode==="glass"){de.classList.add("s67-glass");return}
if(D.getElementById("s67season"))return;
function season(){var s=null;try{if(q&&q!=="demo")sessionStorage.setItem("s67s",q);s=sessionStorage.getItem("s67s")}catch(e){}
 if(s==="autumn"||s==="winter"||s==="spring"||s==="summer")return s;
 var n=new Date(),k=(n.getMonth()+1)*100+n.getDate();return k>=1221||k<320?"winter":k<621?"spring":k<923?"summer":"autumn"}
var S=season(),B="/school67/bg/";
var VS={autumn:["https://assets.mixkit.co/videos/34045/34045-720.mp4"],winter:[],spring:["https://videos.pexels.com/video-files/36496434/15475822_1280_720_30fps.mp4"],summer:["https://videos.pexels.com/video-files/33794003/14344334_1280_720_30fps.mp4"]};
var RM=false;try{RM=W.matchMedia("(prefers-reduced-motion: reduce)").matches}catch(e){}
function go(){if(D.getElementById("s67fpic"))return;de.classList.add("s67bgon","s67-"+S);
 var st=D.createElement("style");st.id="s67fbg";st.textContent="html.s67bgon,html.s67bgon body{background:transparent!important;background-image:none!important}#s67fpic,#s67fvid{position:fixed;top:0;left:0;right:0;bottom:0;width:100%;height:100%;object-fit:cover;z-index:-3;pointer-events:none;background-size:cover;background-position:center}#s67fveil{position:fixed;top:0;left:0;right:0;bottom:0;z-index:-2;pointer-events:none;background:rgba(255,255,255,.42)}@media print{#s67fpic,#s67fvid,#s67fveil{display:none!important}html.s67bgon,html.s67bgon body{background:#fff!important}}";
 (D.head||de).appendChild(st);
 var p=D.createElement("div");p.id="s67fpic";p.style.backgroundImage="url("+B+S+".jpg)";D.body.appendChild(p);
 var ve=D.createElement("div");ve.id="s67fveil";D.body.appendChild(ve);
 if(RM)return;
 var L=VS[S]&&VS[S].length?VS[S]:[B+S+".mp4"],v=D.createElement("video");v.id="s67fvid";v.muted=true;v.loop=true;v.autoplay=true;v.setAttribute("playsinline","");v.setAttribute("muted","");v.setAttribute("aria-hidden","true");v.preload="auto";
 v.onerror=function(){if(v.parentNode)v.parentNode.removeChild(v)};v.src=L[0];D.body.insertBefore(v,ve);
 var pl=v.play&&v.play();if(pl&&pl.catch)pl.catch(function(){});}
if(D.body)go();else D.addEventListener("DOMContentLoaded",go);
})();
