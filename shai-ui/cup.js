
const stage=document.querySelector('.cup-stick'),canvas=document.getElementById('cupC');
const small=matchMedia('(max-width:900px)').matches;
const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;
let started=false;
const io=new IntersectionObserver(es=>{if(es[0].isIntersecting&&!started){started=true;io.disconnect();boot()}},{rootMargin:'1600px 0px'});
io.observe(document.querySelector('.cup'));

const sm=(a,b,x)=>{x=Math.min(1,Math.max(0,(x-a)/(b-a)));return x*x*(3-2*x)};
const lerp=(a,b,t)=>a+(b-a)*t;

async function boot(){
 const [THREE,{GLTFLoader},{MeshoptDecoder},{RoomEnvironment}]=await Promise.all([import('three'),import('three/addons/loaders/GLTFLoader.js'),import('three/addons/libs/meshopt_decoder.module.js'),import('three/addons/environments/RoomEnvironment.js')]);
 const renderer=new THREE.WebGLRenderer({canvas,alpha:true,antialias:true,powerPreference:'high-performance',preserveDrawingBuffer:false});
 renderer.setPixelRatio(Math.min(devicePixelRatio,small?1.75:2));
 renderer.toneMapping=THREE.ACESFilmicToneMapping;renderer.toneMappingExposure=1.05;renderer.outputColorSpace=THREE.SRGBColorSpace;
 const scene=new THREE.Scene();
 const pm=new THREE.PMREMGenerator(renderer);scene.environment=pm.fromScene(new RoomEnvironment(),.04).texture;scene.environmentIntensity=.55;
 const camera=new THREE.PerspectiveCamera(30,1,.01,50);
 const key=new THREE.DirectionalLight(0xffc27a,3.2);key.position.set(2.5,4,2.5);scene.add(key);
 const rim=new THREE.DirectionalLight(0xffa24a,3.4);rim.position.set(-3,1.5,-3);scene.add(rim);
 const fill=new THREE.DirectionalLight(0xbfd2ff,.5);fill.position.set(-2,1,3);scene.add(fill);

 const group=new THREE.Group();scene.add(group);
 let cupMesh=null,liquid=null,R=1,center=new THREE.Vector3(),ready=false;
 const liqMat=new THREE.MeshPhysicalMaterial({color:0xd9b76a,roughness:.06,metalness:0,clearcoat:1,clearcoatRoughness:.05,side:THREE.DoubleSide,emissive:0x4a1c04,emissiveIntensity:.25});
 const prof=[[-.30,0],[-.28,.25],[-.2,.45],[-.1,.55],[0,.60],[.2,.67],[.5,.75]];
 const rAt=y=>{for(let i=1;i<prof.length;i++){if(y<=prof[i][0]){const a=prof[i-1],b=prof[i],t=(y-a[0])/(b[0]-a[0]);return lerp(a[1],b[1],t)}}return prof[prof.length-1][1]};
 const Y0=-.285,Y1=.40;let lastLevel=-1;
 function setLevel(L){
  if(Math.abs(L-lastLevel)<.002)return;lastLevel=L;
  if(liquid){liquid.geometry.dispose();liquid.visible=L>.01}if(L<=.01||!liquid)return;
  const top=lerp(Y0,Y1,L),pts=[new THREE.Vector2(0,Y0)];
  for(let i=0;i<=9;i++){const y=lerp(Y0,top,i/9);pts.push(new THREE.Vector2(Math.max(.01,rAt(y)*.965),y))}
  pts.push(new THREE.Vector2(0,top));
  liquid.geometry=new THREE.LatheGeometry(pts,48);
 }

 // steam
 const N=small?40:64,sp=new Float32Array(N*3),sc=new Float32Array(N*3),life=new Float32Array(N),vel=[];
 for(let i=0;i<N;i++){life[i]=Math.random();vel.push({x:(Math.random()-.5)*.02,z:(Math.random()-.5)*.012,y:.03+Math.random()*.03,ph:Math.random()*6.28})}
 const tx=document.createElement('canvas');tx.width=tx.height=64;const cx=tx.getContext('2d'),gr=cx.createRadialGradient(32,32,0,32,32,32);gr.addColorStop(0,'rgba(255,255,255,1)');gr.addColorStop(1,'rgba(255,255,255,0)');cx.fillStyle=gr;cx.fillRect(0,0,64,64);
 const sg=new THREE.BufferGeometry();sg.setAttribute('position',new THREE.BufferAttribute(sp,3));sg.setAttribute('color',new THREE.BufferAttribute(sc,3));
 const steam=new THREE.Points(sg,new THREE.PointsMaterial({size:.04,map:new THREE.CanvasTexture(tx),vertexColors:true,transparent:true,depthWrite:false,blending:THREE.AdditiveBlending,sizeAttenuation:true}));
 steam.frustumCulled=false;scene.add(steam);

 const loader=new GLTFLoader();loader.setMeshoptDecoder(MeshoptDecoder);
 loader.load('assets/teacup.glb',g=>{
  const m=g.scene;group.add(m);
  m.traverse(o=>{if(o.isMesh){o.frustumCulled=false;if(o.name==='tea_cup')cupMesh=o;if(o.material){o.material.envMapIntensity=1}}});
  const box=new THREE.Box3().setFromObject(m);box.getCenter(center);R=box.getSize(new THREE.Vector3()).length()/2;
  liquid=new THREE.Mesh(new THREE.BufferGeometry(),liqMat);liquid.visible=false;liquid.position.z=.2;cupMesh.add(liquid);
  ready=true;stage.classList.add('cup-ready');resize();
 });

 let w=0,h=0;
 function resize(){
  w=stage.clientWidth;h=stage.clientHeight;renderer.setSize(w,h,false);camera.aspect=w/h;
  if(small)camera.setViewOffset(w,h,0,h*.15,w,h);else camera.setViewOffset(w,h,-w*.2,0,w,h);
  camera.updateProjectionMatrix();
 }
 addEventListener('resize',resize);resize();

 // drag
 let drag=0,vx=0,down=false,lx=0;
 canvas.addEventListener('pointerdown',e=>{down=true;lx=e.clientX;canvas.setPointerCapture(e.pointerId)});
 canvas.addEventListener('pointermove',e=>{if(!down)return;const dx=e.clientX-lx;lx=e.clientX;vx=dx*.008;drag+=vx});
 const up=()=>{down=false};canvas.addEventListener('pointerup',up);canvas.addEventListener('pointercancel',up);

 const K=[[0,58,1.12,20],[.25,44,1.0,95],[.5,28,.78,200],[.75,20,.9,300],[1,12,1.08,410]];
 const key4=(p)=>{for(let i=1;i<K.length;i++){if(p<=K[i][0]){const a=K[i-1],b=K[i],t=sm(0,1,(p-a[0])/(b[0]-a[0]));return [lerp(a[1],b[1],t),lerp(a[2],b[2],t),lerp(a[3],b[3],t)]}}return K[K.length-1].slice(1)};

 let P=0,vis=true,t0=performance.now(),prev=t0;
 new IntersectionObserver(es=>{vis=es[0].isIntersecting}).observe(stage);
 const col0=new THREE.Color(0xc07e24),col1=new THREE.Color(0x5a2205);
 function frame(now){
  requestAnimationFrame(frame);if(!vis||!ready)return;
  const dt=Math.min(.05,(now-prev)/1000);prev=now;
  const tp=window.__cupP||0;P+=(tp-P)*Math.min(1,dt*5);
  if(!down){drag+=vx;vx*=.94}
  const [el,dm,az]=key4(P);
  const dist=R*3.7*dm*(small?.88/Math.min(1,camera.aspect):1);
  const a=THREE.MathUtils.degToRad(az)+drag+(reduce?0:now*.00008),e=THREE.MathUtils.degToRad(el);
  camera.position.set(center.x+dist*Math.cos(e)*Math.sin(a),center.y+dist*Math.sin(e),center.z+dist*Math.cos(e)*Math.cos(a));
  camera.lookAt(center.x,center.y-R*.02,center.z);
  // liquid
  const L=sm(.2,.5,P);setLevel(L);
  const tcol=sm(.45,.75,P);liqMat.color.copy(col0).lerp(col1,tcol);liqMat.emissiveIntensity=.2+.5*tcol;
  // steam
  const sl=L>.9?.25+.75*sm(.6,.85,P):0;
  if(cupMesh&&liquid&&liquid.visible){const top=new THREE.Vector3(0,lerp(Y0,Y1,L),.2);cupMesh.localToWorld(top);
   for(let i=0;i<N;i++){
    life[i]-=dt*.32;if(life[i]<=0){life[i]=1;sp[i*3]=top.x+(Math.random()-.5)*.03;sp[i*3+1]=top.y;sp[i*3+2]=top.z+(Math.random()-.5)*.03}
    const v=vel[i];sp[i*3]+=Math.sin(now*.001+v.ph)*.0004+v.x*dt;sp[i*3+1]+=v.y*dt;sp[i*3+2]+=v.z*dt;
    const f=Math.sin(Math.PI*(1-life[i]))*sl*.05;sc[i*3]=f;sc[i*3+1]=f*.95;sc[i*3+2]=f*.88}
   sg.attributes.position.needsUpdate=true;sg.attributes.color.needsUpdate=true;
   steam.material.size=.05*(R/.12)}
  else steam.visible=true;
  renderer.render(scene,camera);
 }
 requestAnimationFrame(frame);
 window.__cup={renderer,get ready(){return ready}};
}
