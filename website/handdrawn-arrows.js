// Small drawn gestures retain the direction of the original navigation arrows.
(()=>{
 const rotations={'↗':0,'→':45,'↘':90,'↙':180,'↓':135,'↑':-45};
 const draw=text=>{const span=document.createElement('span');span.className='hand-arrow';span.setAttribute('aria-hidden','true');span.style.setProperty('--arrow-turn',`${rotations[text]}deg`);span.innerHTML='<svg viewBox="0 0 64 40" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" focusable="false"><path d="M3 30C17 37 40 29 58 6M45 9C50 9 55 7 59 5C58 10 56 15 57 20"/></svg>';return span;};
 function replace(root){if(root.nodeType===3){if(!/[↗→↘↙↓↑]/.test(root.nodeValue))return;const parts=root.nodeValue.split(/([↗→↘↙↓↑])/);const fragment=document.createDocumentFragment();for(const part of parts)fragment.append(rotations[part]!==undefined?draw(part):document.createTextNode(part));root.replaceWith(fragment);return;}if(root.nodeType!==1)return;if(root.matches('script,style,svg,.hand-arrow,textarea,input'))return;for(const child of [...root.childNodes])replace(child)}
 replace(document.body);new MutationObserver(records=>{for(const record of records){if(record.type==='characterData')replace(record.target);else for(const node of record.addedNodes)replace(node)}}).observe(document.body,{childList:true,subtree:true,characterData:true});
})();
