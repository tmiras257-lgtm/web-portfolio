import * as THREE from 'three';
import {GLTFLoader} from 'three/addons/loaders/GLTFLoader.js';
import {RoomEnvironment} from 'three/addons/environments/RoomEnvironment.js';

export async function start(cv,ready,reduced){
 const r=new THREE.WebGLRenderer({canvas:cv,antialias:true,alpha:true});
 r.setPixelRatio(Math.min(devicePixelRatio,2));r.toneMapping=THREE.ACESFilmicToneMapping;r.toneMappingExposure=1.05;r.shadowMap.enabled=true;r.shadowMap.type=THREE.PCFSoftShadowMap;
 const scene=new THREE.Scene(),cam=new THREE.PerspectiveCamera(32,1,.1,500);
 const pm=new THREE.PMREMGenerator(r);scene.environment=pm.fromScene(new RoomEnvironment(),.04).texture;
 const sun=new THREE.DirectionalLight(0xfff0d8,2.2);sun.position.set(60,110,70);sun.castShadow=true;sun.shadow.mapSize.set(1024,1024);
 Object.assign(sun.shadow.camera,{left:-90,right:90,top:90,bottom:-90,near:10,far:400});sun.shadow.bias=-.0005;scene.add(sun);
 const gltf=await new GLTFLoader().loadAsync('./assets/Fox.glb');
 const fox=gltf.scene;fox.traverse(o=>{if(o.isMesh){o.castShadow=true;o.frustumCulled=false}});
 const box=new THREE.Box3().setFromObject(fox),size=box.getSize(new THREE.Vector3()),ctr=box.getCenter(new THREE.Vector3());
 const g=new THREE.Group();fox.position.set(-ctr.x,-box.min.y,-ctr.z);g.add(fox);scene.add(g);
 const H=size.y,L=Math.max(size.x,size.z);
 const sh=new THREE.Mesh(new THREE.CircleGeometry(L*.9,48).rotateX(-Math.PI/2),new THREE.ShadowMaterial({opacity:.28}));sh.receiveShadow=true;sh.position.y=.2;scene.add(sh);
 const mixer=new THREE.AnimationMixer(fox),acts=gltf.animations.map(c=>mixer.clipAction(c));
 let curA=null;
 function setAnim(i){const n=acts[i];if(!n||n===curA)return;n.reset().setEffectiveWeight(1).play();if(curA)curA.crossFadeTo(n,.5,false);curA=n;
  mixer.timeScale=i==2?1:1}
 const target=new THREE.Vector3(0,H*.42,0);let dist=0;
 function fit(){const w=cv.clientWidth,h=cv.clientHeight;r.setSize(w,h,false);cam.aspect=w/h;cam.updateProjectionMatrix();dist=Math.max(H*2.0,L*1.75)/Math.min(1,cam.aspect*1.1)*1.05;}
 new ResizeObserver(fit).observe(cv);fit();
 let yaw=-.6,vel=0,drag=false,lx=0,mx=0,my=0;
 cv.addEventListener('pointerdown',e=>{drag=true;lx=e.clientX;cv.setPointerCapture(e.pointerId);cv.parentElement.style.cursor='grabbing'});
 cv.addEventListener('pointermove',e=>{if(drag){vel=(e.clientX-lx)*.012;yaw+=vel;lx=e.clientX}const b=cv.getBoundingClientRect();mx=((e.clientX-b.left)/b.width-.5);my=((e.clientY-b.top)/b.height-.5)});
 const up=()=>{drag=false;cv.parentElement.style.cursor=''};cv.addEventListener('pointerup',up);cv.addEventListener('pointercancel',up);
 const clock=new THREE.Clock();let vis=true;new IntersectionObserver(es=>{vis=es[0].isIntersecting}).observe(cv);
 function loop(){requestAnimationFrame(loop);if(!vis)return;const dt=clock.getDelta();mixer.update(reduced?0:dt);
  if(!drag){vel*=.94;yaw+=vel+(reduced?0:dt*.35)}
  const a=yaw,tx=Math.sin(a)*dist,tz=Math.cos(a)*dist,ty=H*.55+(-my*H*.25);
  cam.position.set(tx+mx*0,ty,tz);cam.lookAt(target);r.render(scene,cam)}
 setAnim(0);ready(setAnim);loop();
}
