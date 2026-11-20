// МЕРА: real GLB (Khronos SheenChair, CC0) + Poly Haven HDRI (CC0). Drag / scroll / palette-tinted fabric.
import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RGBELoader} from 'three/addons/loaders/RGBELoader.js';
export async function start(canvas,box,onReady){
 const R=new THREE.WebGLRenderer({canvas,antialias:true,alpha:true});
 R.setPixelRatio(Math.min(devicePixelRatio,2));R.toneMapping=THREE.ACESFilmicToneMapping;R.toneMappingExposure=1.0;
 R.shadowMap.enabled=true;R.shadowMap.type=THREE.PCFSoftShadowMap;R.outputColorSpace=THREE.SRGBColorSpace;
 const S=new THREE.Scene(),C=new THREE.PerspectiveCamera(28,1,.1,50);
 const hdr=await new RGBELoader().loadAsync('assets/studio_small_09_1k.hdr');hdr.mapping=THREE.EquirectangularReflectionMapping;
 S.environment=new THREE.PMREMGenerator(R).fromEquirectangular(hdr).texture;S.environmentIntensity=1.1;
 const key=new THREE.DirectionalLight(0xfff3e0,2.4);key.position.set(3,6,4);key.castShadow=true;key.shadow.mapSize.set(1024,1024);
 Object.assign(key.shadow.camera,{left:-3,right:3,top:3,bottom:-3,near:1,far:15});key.shadow.radius=8;key.shadow.bias=-.0005;S.add(key);
 const g=await new GLTFLoader().loadAsync('assets/SheenChair.glb');const chair=g.scene;
 const b=new THREE.Box3().setFromObject(chair),sz=b.getSize(new THREE.Vector3()),c=b.getCenter(new THREE.Vector3());
 const k=2.2/Math.max(sz.x,sz.y,sz.z);chair.scale.setScalar(k);chair.position.set(-c.x*k,-b.min.y*k,-c.z*k);
 const fab=[];chair.traverse(o=>{if(o.isMesh){o.castShadow=true;(Array.isArray(o.material)?o.material:[o.material]).forEach(m=>{if(/fabric/i.test(m.name))fab.push(m)})}});
 const grp=new THREE.Group();grp.add(chair);S.add(grp);
 const floor=new THREE.Mesh(new THREE.CircleGeometry(5,48),new THREE.ShadowMaterial({opacity:.28}));floor.rotation.x=-Math.PI/2;floor.receiveShadow=true;S.add(floor);
 const size=()=>{const r=canvas.getBoundingClientRect();R.setSize(r.width,r.height,false);C.aspect=r.width/r.height;C.updateProjectionMatrix();C.position.set(0,1.5,5.2/Math.min(1,C.aspect*1.05));C.lookAt(0,.95,0)};
 size();addEventListener('resize',size);
 // palette tint
 window.meraTint=hex=>{const col=new THREE.Color(hex);fab.forEach(m=>{m.color.copy(col).multiplyScalar(1.0);if(m.sheenColor)m.sheenColor.copy(col).lerp(new THREE.Color(1,1,1),.35);m.needsUpdate=true})};
 if(window.__tint)window.meraTint(window.__tint);
 let rot=.7,vel=0,drag=false,lx=0,vis=true;
 new IntersectionObserver(e=>vis=e[0].isIntersecting).observe(box);
 box.addEventListener('pointerdown',e=>{drag=true;lx=e.clientX;box.setPointerCapture(e.pointerId)});
 box.addEventListener('pointermove',e=>{if(!drag)return;vel=(e.clientX-lx)*.012;rot+=vel;lx=e.clientX});
 const up=()=>drag=false;box.addEventListener('pointerup',up);box.addEventListener('pointercancel',up);
 const reduce=matchMedia('(prefers-reduced-motion:reduce)').matches;let lastY=scrollY;
 const frame=()=>{requestAnimationFrame(frame);if(!vis)return;const dy=scrollY-lastY;lastY=scrollY;
  if(!drag){vel*=.92;rot+=vel+(reduce?0:.004)+dy*.0016}
  grp.rotation.y=rot;R.render(S,C)};
 requestAnimationFrame(frame);onReady&&onReady();
}
