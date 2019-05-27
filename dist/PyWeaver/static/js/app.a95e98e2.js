(function(e){function t(t){for(var n,s,r=t[0],c=t[1],d=t[2],u=0,p=[];u<r.length;u++)s=r[u],a[s]&&p.push(a[s][0]),a[s]=0;for(n in c)Object.prototype.hasOwnProperty.call(c,n)&&(e[n]=c[n]);l&&l(t);while(p.length)p.shift()();return i.push.apply(i,d||[]),o()}function o(){for(var e,t=0;t<i.length;t++){for(var o=i[t],n=!0,r=1;r<o.length;r++){var c=o[r];0!==a[c]&&(n=!1)}n&&(i.splice(t--,1),e=s(s.s=o[0]))}return e}var n={},a={app:0},i=[];function s(t){if(n[t])return n[t].exports;var o=n[t]={i:t,l:!1,exports:{}};return e[t].call(o.exports,o,o.exports,s),o.l=!0,o.exports}s.m=e,s.c=n,s.d=function(e,t,o){s.o(e,t)||Object.defineProperty(e,t,{enumerable:!0,get:o})},s.r=function(e){"undefined"!==typeof Symbol&&Symbol.toStringTag&&Object.defineProperty(e,Symbol.toStringTag,{value:"Module"}),Object.defineProperty(e,"__esModule",{value:!0})},s.t=function(e,t){if(1&t&&(e=s(e)),8&t)return e;if(4&t&&"object"===typeof e&&e&&e.__esModule)return e;var o=Object.create(null);if(s.r(o),Object.defineProperty(o,"default",{enumerable:!0,value:e}),2&t&&"string"!=typeof e)for(var n in e)s.d(o,n,function(t){return e[t]}.bind(null,n));return o},s.n=function(e){var t=e&&e.__esModule?function(){return e["default"]}:function(){return e};return s.d(t,"a",t),t},s.o=function(e,t){return Object.prototype.hasOwnProperty.call(e,t)},s.p="/";var r=window["webpackJsonp"]=window["webpackJsonp"]||[],c=r.push.bind(r);r.push=t,r=r.slice();for(var d=0;d<r.length;d++)t(r[d]);var l=c;i.push([0,"chunk-vendors"]),o()})({0:function(e,t,o){e.exports=o("56d7")},"034f":function(e,t,o){"use strict";var n=o("1356"),a=o.n(n);a.a},1:function(e,t){},1356:function(e,t,o){},"56d7":function(e,t,o){"use strict";o.r(t);o("cadf"),o("551c"),o("f751"),o("097d");var n=o("a026"),a=o("bb71"),i=o("8336");o("da64");n["a"].use(a["a"],{iconfont:"md",components:{VBtn:i["a"]}});var s=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("v-app",[o("v-toolbar",{attrs:{app:"",dark:"",fixed:"","clipped-left":""}},[o("v-toolbar-title",{staticClass:"headline text-uppercase"},[o("span",[e._v("Py")]),o("span",{staticClass:"font-weight-light"},[e._v("Weaver")]),o("span",[e._v("2")])]),o("v-spacer"),o("v-toolbar-items",[o("v-btn",{attrs:{flat:"",small:""},on:{click:e.OpenFile}},[o("span",[e._v("Open file")]),o("v-icon",[e._v("folder_open")])],1),o("v-btn",{attrs:{flat:"",small:""},on:{click:e.SaveModel}},[o("span",[e._v("Save model")]),o("v-icon",[e._v("cloud_download")])],1)],1),e.connected?o("v-chip",{attrs:{color:"green","text-color":"white"}},[e._v("Connected")]):e._e(),e.connected?e._e():o("v-chip",{attrs:{color:"red","text-color":"white"}},[e._v("Disconnected")])],1),o("input",{attrs:{type:"file",id:"fileInput",hidden:""},on:{change:function(t){return e.OpenModel(t)}}}),o("SideBar"),o("v-content",{attrs:{app:""}},[o("v-card",{attrs:{height:"100%"}},[o("div",{staticStyle:{width:"100%",height:"100%"},attrs:{id:"canvas"}})])],1),o("CodeEditor"),o("LibrarySaveDialog"),o("v-footer",{staticClass:"pa-3",attrs:{app:"",dark:""}},[o("v-btn",{attrs:{color:"gray",dark:""},on:{click:e.resetServer}},[e._v("Reset")]),o("v-spacer"),o("div",[e._v("© "+e._s((new Date).getFullYear()))])],1)],1)},r=[],c=(o("6762"),o("2fdb"),o("d225")),d=o("b0b4"),l=new n["a"],u=function(){function e(t,o){Object(c["a"])(this,e),this.container=t,this.graph={},this.store=o,this.codeNode={}}return Object(d["a"])(e,[{key:"GetModelXML",value:function(){var e=this.graph,t=new mxCodec,o=t.encode(e.getModel()),n=mxUtils.getPrettyXml(o);return n}},{key:"LoadModel",value:function(e){var t=this.graph,o=e,n=mxUtils.parseXml(o),a=n.documentElement,i=new mxCodec(a.ownerDocument);i.decode(a,t.getModel())}},{key:"mount",value:function(){var e=this;mxEvent.disableContextMenu(this.container),mxGraph.prototype.isCellMovable=function(e){if(this.lastEvent.altKey)return!1;var t=this.view.getState(e),o=null!=t?t.style:this.getCellStyle(e);return this.isCellsMovable()&&!this.isCellLocked(e)&&0!=o[mxConstants.STYLE_MOVABLE]};var t=new mxGraph(this.container);this.graph=t,t.store=this.store,t.setAllowDanglingEdges(!1),t.setConnectable(!0),t.setMultigraph(!0),t.isCellEditable=function(e){return!1},t.htmlLabels=!0,t.autoSizeCells=!0,t.foldingEnabled=!1;var o=t.getStylesheet().getDefaultVertexStyle();o["fillColor"]="#FFFFFF",o["strokeColor"]="#000000",o["fontColor"]="#000000",o["fontStyle"]="1",o=t.getStylesheet().getDefaultEdgeStyle(),o["strokeColor"]="#000000",o["fontColor"]="#000000",o["fontStyle"]="0",o["fontStyle"]="0",o["startSize"]="8",o["endSize"]="8",o[mxConstants.STYLE_ROUNDED]=!0,o[mxConstants.STYLE_EDGE]=mxEdgeStyle.EntityRelation,o[mxConstants.STYLE_STROKEWIDTH]="1",o[mxConstants.STYLE_LABEL_BACKGROUNDCOLOR]="#FFFFFF",mxRubberband.prototype.isForceRubberbandEvent=function(e){return!1},new mxRubberband(t),t.isPort=function(e){this.getCellGeometry(e);return!1},mxEvent.addMouseWheelListener(mxUtils.bind(this,function(e,o){1==e.altKey&&(1==o?t.zoomIn():t.zoomOut())}));var n=new mxKeyHandler(t);n.bindKey(46,function(e){t.isEnabled()&&t.removeCells()}),t.connectionHandler.addListener(mxEvent.CONNECT,function(t,o){var n=o.getProperty("cell"),a={source_id:n.source.parent.id,target_id:n.target.parent.id,source_var:n.source.value,target_var:n.target.value};e.store.dispatch("add_connection",a)}),t.addListener(mxEvent.DOUBLE_CLICK,function(t,o){var n=o.getProperty("cell");if(null!=n&&n.isNode){var a=e.store.state.code_nodes[n.id];e.store.dispatch("open_code_editor",a)}}),t.addListener(mxEvent.MOUSE_MOVE,function(e,o){t.isMouseDown&&console.log("yay")}),t.addListener(mxEvent.CELLS_REMOVED,function(t,o){for(var n=o.properties.cells,a=0;a<n.length;a++){var i=n[a];if(i.edge){var s={source_id:i.source.parent.id,source_var:i.source.value,target_id:i.target.parent.id,target_var:i.target.value};e.store.dispatch("remove_connection",s)}}for(a=0;a<n.length;a++){i=n[a];i.isNode&&e.store.dispatch("delete_node",i.id)}})}},{key:"addNode",value:function(e){var t=null,o=this.graph.getDefaultParent();this.graph.getModel().beginUpdate();try{var n=[],a=[];for(var i in e.outputs)n.push(i);for(var i in e.inputs)a.push(i);var s=30*Math.max(n.length,a.length)+40;t=this.graph.insertVertex(o,null,"",20,20,80,s,"verticalAlign=top");t.value="<div id='node_"+t.id+"'></div>",t.display_act_code="",t.setConnectable(!1),t.isNode=!0}finally{this.graph.getModel().endUpdate()}return this.changePorts(t,n,1,"output"),this.changePorts(t,a,0,"input"),t}},{key:"changePorts",value:function(e,t,o,n){var a=this.graph.getModel(),i=[],s=[],r="";r=0==o?"labelPosition=right;align=left;deletable=0":"labelPosition=left;align=right;deletable=0",this.graph.getModel().beginUpdate();try{if(e.children)for(var c=0;c<e.children.length;c++){var d=e.children[c],l=d.value,u=d.tag;t.includes(l)||u!=n?u==n&&(s.push(d),i.push(l)):(this.graph.removeCells(a.getEdges(d),!1),this.graph.removeCells([d],!1),c-=1)}for(c=0;c<t.length;c++){l=t[c];if(i.includes(l)){p=s[c];p.geometry.y=1/(t.length+1)*(c+1)}else{var p=this.graph.insertVertex(e,null,l,o,1/(t.length+1)*(c+1),10,10,r,!0);p.geometry.offset=new mxPoint(-5,-5),p.setConnectable(!0),p.tag=n}}this.graph.getView().validate()}finally{this.graph.getModel().endUpdate()}}},{key:"updateCell",value:function(e){this.graph.getView().clear(e,!1,!1),this.graph.getView().validate()}}]),e}(),p=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("v-dialog",{attrs:{width:"800",persistent:""},on:{keydown:e.codeDialogShortcuts},model:{value:e.code_dialog,callback:function(t){e.code_dialog=t},expression:"code_dialog"}},[o("v-card",[o("v-toolbar",{attrs:{dark:"",color:"gray"}},[o("v-toolbar-title",[e._v("Editor")]),o("v-btn",{attrs:{icon:""},on:{click:e.openSaveDialog}},[o("v-icon",[e._v("save")])],1),o("v-spacer"),o("v-toolbar-items",[o("v-btn",{attrs:{icon:"",dark:""},on:{click:e.closeDialog}},[o("v-icon",[e._v("close")])],1)],1)],1),o("v-card-text",[o("v-tabs",{attrs:{dark:""}},[o("v-tab",[e._v("Code")]),o("v-tab-item",[o("codemirror",{ref:"code_editor",attrs:{options:e.cmOptions},model:{value:e.code,callback:function(t){e.code=t},expression:"code"}})],1),o("v-tab",[e._v("Display")]),o("v-tab-item",[o("codemirror",{ref:"code_editor",attrs:{options:e.dispCmOptions},model:{value:e.display_code,callback:function(t){e.display_code=t},expression:"display_code"}})],1),o("v-tab",[e._v("Display Actions")]),o("v-tab-item",[o("codemirror",{ref:"code_editor",attrs:{options:e.dispActCmOptions},model:{value:e.display_act_code,callback:function(t){e.display_act_code=t},expression:"display_act_code"}})],1)],1),o("v-spacer")],1),o("v-card-actions",[o("v-spacer"),o("v-btn",{attrs:{color:"green",flat:"",dark:""},on:{click:e.saveCode}},[e._v("Update")])],1)],1)],1)},_=[],v=(o("a7be"),o("db91"),o("8c2e"),o("d69f"),o("f9d4"),o("8f94")),h={components:{codemirror:v["codemirror"]},data:function(){return{cmOptions:{tabSize:4,indentUnit:4,mode:"python",lineNumbers:!0,indentWithTabs:!0,viewportMargin:1/0,line:!0,theme:"base16-dark",autoRefresh:!0},dispCmOptions:{tabSize:4,indentUnit:4,mode:"htmlmixed",lineNumbers:!0,indentWithTabs:!0,viewportMargin:1/0,line:!0,theme:"base16-dark",autoRefresh:!0},dispActCmOptions:{tabSize:4,indentUnit:4,mode:"javascript",lineNumbers:!0,indentWithTabs:!0,viewportMargin:1/0,line:!0,theme:"base16-dark",autoRefresh:!0}}},methods:{closeDialog:function(){this.code_dialog=!1},openSaveDialog:function(){this.$store.commit("set_dialog_open",!0)},saveCode:function(){this.$store.dispatch("save_node_code",{code:this.code,display_code:this.display_code,display_act_code:this.display_act_code}),this.closeDialog()},codeDialogShortcuts:function(e){13===e.keyCode&&e.shiftKey?this.saveCode():27===e.keyCode&&this.closeDialog()}},computed:{code:{get:function(){return this.$store.state.code},set:function(e){this.$store.commit("set_code",e)}},display_code:{get:function(){return this.$store.state.display_code},set:function(e){this.$store.commit("set_display_code",e)}},display_act_code:{get:function(){return this.$store.state.display_act_code},set:function(e){this.$store.commit("set_display_act_code",e)}},code_dialog:{get:function(){return this.$store.state.open_code_editor},set:function(e){this.$store.commit("open_editor",e)}}}},f=h,m=o("2877"),y=o("6544"),g=o.n(y),b=o("b0af"),x=o("99d9"),C=o("169a"),k=o("132d"),w=o("9910"),S=o("71a3"),$=o("c671"),D=o("fe57"),V=o("71d9"),T=o("2a7f"),E=Object(m["a"])(f,p,_,!1,null,null,null),O=E.exports;g()(E,{VBtn:i["a"],VCard:b["a"],VCardActions:x["a"],VCardText:x["b"],VDialog:C["a"],VIcon:k["a"],VSpacer:w["a"],VTab:S["a"],VTabItem:$["a"],VTabs:D["a"],VToolbar:V["a"],VToolbarItems:T["a"],VToolbarTitle:T["b"]});var L=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("v-navigation-drawer",{attrs:{permanent:"",clipped:"",dark:"",app:"",width:"300","mini-variant":e.drawer_mini}},[o("v-list",[o("v-list-tile",[o("v-list-tile-content"),o("v-list-tile-action",{on:{click:e.toggleMiniDrawer}},[o("v-btn",{attrs:{icon:""}},[e.drawer_mini?o("v-icon",[e._v("keyboard_arrow_right")]):e._e(),e.drawer_mini?e._e():o("v-icon",[e._v("keyboard_arrow_left")])],1)],1)],1),o("v-list-tile",[o("v-list-tile-content",[o("br"),o("br"),o("v-text-field",{attrs:{label:"Document name"},model:{value:e.document_name,callback:function(t){e.document_name=t},expression:"document_name"}}),o("br")],1)],1),o("v-divider"),o("v-list-tile",{on:{click:e.addNode,keydown:function(t){return!t.type.indexOf("key")&&e._k(t.keyCode,"enter",13,t.key,"Enter")?null:t.shiftKey?e.canvasShortcuts(t):null}}},[o("v-list-tile-action",[o("v-btn",{staticClass:"text-lg-right",attrs:{icon:""}},[o("v-icon",[e._v("add")])],1)],1),o("v-list-tile-content",[e._v("ADD EMPTY NODE")])],1),o("v-card",{directives:[{name:"show",rawName:"v-show",value:!e.drawer_mini,expression:"!drawer_mini"}],staticStyle:{"overflow-y":"scroll"},attrs:{height:"300px"}},[o("v-treeview",{ref:"tree",attrs:{items:e.items},scopedSlots:e._u([{key:"prepend",fn:function(t){var n=t.item;return[n.children?o("v-icon",[e._v("folder")]):e._e(),n.children?e._e():o("v-icon",[e._v("insert_drive_file")])]}},{key:"label",fn:function(t){var n=t.item;return[e._v("\n           "+e._s(n.name)+"\n           "),n.children?e._e():o("v-btn",{attrs:{icon:""},on:{click:function(t){return e.addLibraryNode(n.lib_id)}}},[o("v-icon",[e._v("add_circle_outline")])],1)]}}])})],1),o("v-list-tile",{on:{click:e.runServer}},[o("v-list-tile-action",[o("v-btn",{staticClass:"text-lg-right",attrs:{icon:""}},[o("v-icon",[e._v("computer")])],1)],1),o("v-list-tile-content",[e._v("RUN")])],1),o("v-divider"),o("v-list-tile",[o("v-list-tile-action",[o("v-btn",{staticClass:"text-lg-right",attrs:{icon:""}},[o("v-icon",[e._v("settings")])],1)],1),o("v-list-tile-content",[e._v("SETTINGS")])],1)],1)],1)},M=[],A={mounted:function(){},data:function(){return{drawer_mini:!0,document_name:""}},methods:{addNode:function(){this.$store.dispatch("add_empty_node")},runServer:function(){this.$store.dispatch("execute_server")},resetServer:function(){this.$socket.emit("reset")},toggleMiniDrawer:function(){this.drawer_mini=!this.drawer_mini},addLibraryNode:function(e){this.$socket.emit("get_template",e,this.addNodeAction)},addNodeAction:function(e){this.$store.dispatch("add_node",e)}},computed:{items:{get:function(){return this.$store.state.libraryTree}}}},N=A,P=o("ce7e"),j=o("8860"),I=o("ba95"),R=o("40fe"),F=o("5d23"),U=o("f774"),B=o("2677"),Y=o("eb2a"),K=Object(m["a"])(N,L,M,!1,null,null,null),z=K.exports;g()(K,{VBtn:i["a"],VCard:b["a"],VDivider:P["a"],VIcon:k["a"],VList:j["a"],VListTile:I["a"],VListTileAction:R["a"],VListTileContent:F["a"],VNavigationDrawer:U["a"],VTextField:B["a"],VTreeview:Y["a"]});var G=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("v-dialog",{attrs:{width:"800",persistent:""},model:{value:e.save_dialog,callback:function(t){e.save_dialog=t},expression:"save_dialog"}},[o("v-card",[o("v-toolbar",{attrs:{dark:"",color:"gray"}},[o("v-toolbar-title",[e._v("Save to Library")]),o("v-spacer"),o("v-toolbar-items",[o("v-btn",{attrs:{icon:"",dark:""},on:{click:e.closeDialog}},[o("v-icon",[e._v("close")])],1)],1)],1),o("v-card-text",[o("v-text-field",{attrs:{label:"Node",rules:[e.rules.required]},model:{value:e.save_name,callback:function(t){e.save_name=t},expression:"save_name"}}),o("v-card",{staticStyle:{"overflow-y":"scroll"},attrs:{height:"300px",flat:""}},[o("v-treeview",{ref:"tree",attrs:{items:e.libraryTree,activatable:"",active:e.selected_folder,"return-object":""},on:{"update:active":function(t){e.selected_folder=t}},scopedSlots:e._u([{key:"prepend",fn:function(t){var n=t.item;return[n.children?o("v-icon",[e._v("folder")]):e._e(),n.children?e._e():o("v-icon",[e._v("insert_drive_file")])]}},{key:"label",fn:function(t){var n=t.item;return[e._e(),o("span",[e._v(e._s(n.name))])]}}])})],1)],1),o("v-card-actions",[o("v-spacer"),o("v-btn",{attrs:{color:"blue",flat:"",dark:""},on:{click:e.saveNode}},[e._v("Save")])],1)],1)],1)},W=[],q={data:function(){return{selected_folder:[],rename_dialog:!1,name_dialog:!1,save_name:"",rules:{required:function(e){return!!e||"Required."}}}},methods:{closeDialog:function(){this.$store.commit("set_dialog_open",!1)},saveNode:function(){if(this.save_name){var e={},t={},o=this.$store.state.selected_node;t.name=this.save_name,t.code=o.code,t.display_code=o.display_code,t.display_act_code=o.display_act_code;var n=this.selected_folder[0].path;e.path=n,e.node_data=t,this.$socket.emit("save_to_library",e),this.closeDialog()}}},computed:{save_dialog:{get:function(){return this.$store.state.save_dialog}},libraryTree:{get:function(){return this.$store.state.libraryTree}}}},X=q,H=Object(m["a"])(X,G,W,!1,null,null,null),J=H.exports;g()(H,{VBtn:i["a"],VCard:b["a"],VCardActions:x["a"],VCardText:x["b"],VDialog:C["a"],VIcon:k["a"],VSpacer:w["a"],VTextField:B["a"],VToolbar:V["a"],VToolbarItems:T["a"],VToolbarTitle:T["b"],VTreeview:Y["a"]});var Q={name:"App",components:{CodeEditor:O,SideBar:z,LibrarySaveDialog:J},data:function(){return{connected:!1}},mounted:function(){var e=document.getElementById("canvas"),t=new u(e,this.$store);t.mount(),this.$store.commit("set_canvas",t)},methods:{OpenFile:function(){var e=document.getElementById("fileInput");e.click()},OpenModel:function(e){var t=this,o=e.target.files[0];if(o){var n=new FileReader;n.onload=function(e){var o=e.target.result;t.$store.state.canvas.LoadModel(o)},n.readAsText(o)}},resetServer:function(){this.$socket.emit("reset")},SaveModel:function(){var e=this.$store.state.canvas.GetModelXML(),t=document.createElement("a");t.setAttribute("href","data:text/plain;charset=utf-8,"+encodeURIComponent(e));var o=this.$store.state.document_name+".xml";t.setAttribute("download",o),t.style.display="none",document.body.appendChild(t),t.click(),document.body.removeChild(t)}},computed:{document_name:{get:function(){return this.$store.state.document_name},set:function(e){this.$store.commit("set_document_name",e)}}},watch:{code_dialog:function(e,t){var o=this;if(e)return setTimeout(function(){o.$refs.code_editor.codemirror.refresh(),o.$refs.code_editor.codemirror.focus()},200)}},sockets:{connect:function(){this.connected=!0},disconnect:function(){this.connected=!1}}},Z=Q,ee=(o("034f"),o("7496")),te=o("cc20"),oe=o("549c"),ne=o("553a"),ae=Object(m["a"])(Z,s,r,!1,null,null,null),ie=ae.exports;g()(ae,{VApp:ee["a"],VBtn:i["a"],VCard:b["a"],VChip:te["a"],VContent:oe["a"],VFooter:ne["a"],VIcon:k["a"],VSpacer:w["a"],VToolbar:V["a"],VToolbarItems:T["a"],VToolbarTitle:T["b"]});var se=o("2f62"),re="node_id",ce="is_variable",de="param_name",le="PyWeaverNodeDisplay",ue={DISPLAY_NODE_ID_ATTR:re,DISPLAY_VAR_ATTR:ce,DISPLAY_VAR_NAME_ATTR:de,DISPLAY_CLASS:le},pe=function(){function e(t,o,n){Object(c["a"])(this,e),this.canvas=o,this.id="",this.inputs={},this.outputs={},this.code_source="local",this.code="",this.display_code=t,this.display_act_code="",this.cell_id="",this.cell={},this.compiled_display_code="",this.compileDisplayCode(),this.store=n}return Object(d["a"])(e,[{key:"setCell",value:function(e){this.cell=e,this.id=e.id}},{key:"compileDisplayCode",value:function(){this.compiled_display_code="<div "+ue.DISPLAY_NODE_ID_ATTR+"='"+this.cell.id+"' class='"+ue.DISPLAY_CLASS+"'id='node_"+this.cell.id+"'>"+this.display_code+"</div>"}},{key:"setCode",value:function(e){this.code=e,this.cell.code=e}},{key:"setDisplayCode",value:function(e){this.display_code=e,this.compileDisplayCode(),this.cell.display_code=e}},{key:"setDisplayActCode",value:function(e){this.display_act_code=e,this.cell.display_act_code=e}}]),e}(),_e=o("8055"),ve=o.n(_e),he=ve()("http://localhost:5000"),fe=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",{key:e.run_id},[o("v-runtime-template",{attrs:{template:e.template,display_code:e.display_code}})],1)},me=[],ye=(o("7f7f"),o("ac6a"),o("456d"),o("75fc")),ge={bind:function(e,t,o){o.context["scope"][t.arg]||(o.context["scope"][t.arg]=t.value)}};n["a"].directive("val",ge);var be=o("61cc"),xe=o.n(be),Ce=function(e){return[].concat(Object(ye["a"])(Object.keys(e.data&&e.data()||{})),Object(ye["a"])(Object.keys(e.props||{})))},ke=function(e,t,o){if(!t.hasOwnProperty(o)){var n=Object.getOwnPropertyDescriptor(e,o);Object.defineProperty(t,o,n)}},we=function(e){var t={};return e.forEach(function(e){e&&Object.getOwnPropertyNames(e).forEach(function(o){return ke(e,t,o)})}),t},Se=function(e,t){var o={};return t.forEach(function(t){return ke(e,o,t)}),o},$e={props:{template:String,display_code:String},directives:{Val:ge},data:function(){return{plotly:xe.a}},render:function(e){if(this.template){var t=this.$parent,o=t.$data,n=t.$props,a=t.$options,i="{}";if(this.display_code&&(i=this.display_code),i!=this.$parent.$data._previous_display_code){var s="function(){return "+this.$parent.$data._previous_display_code+" }();",r=Function("return "+s)();for(var c in r)delete a.methods[c],delete this.$parent[c];this.$parent.$data._previous_display_code=i,s="function(){return "+i+" }();";var d=Function("return "+s)();for(var c in d){var l=d[c].bind(this.$parent);a.methods[c]=l,this.$parent[c]=l}}this.$parent.$data._previous_template!=this.template&&(this.$parent.$data.scope={},this.$parent.$data._previous_template=this.template);var u=Object.keys(a.methods||{}),p=Ce(a).concat(u),_=Se(this.$parent,u),v=we([o,n,_]),h={template:this.template||"<div></div>",props:p,computed:a.computed,components:a.components};return e(h,{props:v})}}},De={props:["_node","store"],data:function(){return{id:"",template:"<div>Node</div>",display_code:"{}",scope:{},node:{},_previous_template:"",_previous_display_code:"{}"}},components:{VRuntimeTemplate:$e},directives:{Val:ge},methods:{changeCode:function(e){this.template="<div>"+e+"</div>"},changeAct:function(e){this.display_code=e},updateDisplay:function(){this.$forceUpdate(),this.onResults&&this.onResults()}},computed:{run_id:function(){return this.store.state.run_id}},mounted:function(){this.node=new Proxy(this._node,{get:function(e,t,o){var n=null;if("__ob__"!=t){var a=null,i=null;if(t in e.inputs){console.log("input request");var s=e.inputs[t];s&&(a=s.id,i=s.var_name)}else a=e.id,i=t;a&&i&&a in e.store.state.results&&i in e.store.state.results[a]&&(n=e.store.state.results[a][i])}return n}})}},Ve=De,Te=Object(m["a"])(Ve,fe,me,!1,null,null,null),Ee=Te.exports;n["a"].use(se["a"]);var Oe=new se["a"].Store({state:{canvas:{},selected_node:{},open_code_editor:!1,code:"",display_code:"",display_act_code:"",code_nodes:{},document_name:"Untitled",node_displays:{},results:{},auto_exec:!1,run_id:0,libraryTree:[],save_dialog:!1},mutations:{tree_change:function(e,t){e.libraryTree=t},set_selected_node:function(e,t){e.selected_node=t},open_editor:function(e,t){e.open_code_editor=t},set_dialog_open:function(e,t){e.save_dialog=t},set_canvas:function(e,t){e.canvas=t},set_code:function(e,t){e.code=t},set_display_code:function(e,t){e.display_code=t},set_display_act_code:function(e,t){e.display_act_code=t},set_document_name:function(e,t){e.document_name=t}},actions:{open_code_editor:function(e,t){e.commit("set_selected_node",t),e.commit("set_code",t.code),e.commit("set_display_code",t.display_code),e.commit("set_display_act_code",t.display_act_code),e.commit("open_editor",!0)},add_empty_node:function(e){var t=e.state.canvas,o=new pe("Node",e.state.canvas,e),a=t.addNode(o),i=a.id,s=n["a"].extend(Ee),r=new s({propsData:{_node:o,store:e}});r.$mount(),document.getElementById("node_"+i).appendChild(r.$el),e.state.node_displays[a.id]=r,e.state.code_nodes[a.id]=o,o.setCell(a),he.emit("new_node",a.id)},add_node:function(e,t){var o=e.state.canvas,a=new pe("Node",e.state.canvas,e),i=o.addNode(a),s=i.id,r=n["a"].extend(Ee),c=new r({propsData:{_node:a,store:e}});c.$mount(),document.getElementById("node_"+s).appendChild(c.$el),e.state.node_displays[i.id]=c,e.state.code_nodes[i.id]=a,a.setCell(i),e.commit("set_selected_node",a),he.emit("new_node",i.id),e.dispatch("save_node_code",t)},socket_setLibraryTree:function(e,t){e.commit("tree_change",t)},socket_changeNodeInputPorts:function(e,t){var o=e.state.canvas,n=e.state.selected_node.cell.id,a=e.state.code_nodes[n].cell;for(var i in e.state.code_nodes[n].inputs={},t)e.state.code_nodes[n].inputs[t[i]]=null;o.changePorts(a,t,0,"input")},socket_changeNodeOutputPorts:function(e,t){var o=e.state.canvas,n=e.state.selected_node.cell.id,a=e.state.code_nodes[n].cell;for(var i in e.state.code_nodes[n].outputs={},t)e.state.code_nodes[n].outputs[t[i]]=null;o.changePorts(a,t,1,"output")},save_node_code:function(e,t){e.state.selected_node.setCode(t.code);var o=e.state.selected_node.id;e.state.node_displays[o].changeCode(t.display_code),e.state.selected_node.setDisplayCode(t.display_code),e.state.node_displays[o].changeAct(t.display_act_code),e.state.selected_node.setDisplayActCode(t.display_act_code),e.state.node_displays[o].updateDisplay(),l.$emit("update_displays"),n["a"].nextTick().then(function(){var o={};o.code=t.code,o.id=e.state.selected_node.cell.id,he.emit("edit_node_code",o),e.dispatch("auto_execute")})},add_connection:function(e,t){he.emit("make_connection",t),e.state.code_nodes[t.target_id].inputs[t.target_var]={id:t.source_id,var_name:t.source_var},e.dispatch("auto_execute")},remove_connection:function(e,t){he.emit("delete_connection",t),e.dispatch("auto_execute")},execute_server:function(e){var t={},o=e.state.node_displays;for(var n in o)t[n]=o[n].scope;he.emit("execute",t,function(t){e.state.results=t,e.state.run_id+=1,l.$emit("update_displays")})},auto_execute:function(e){e.state.auto_exec&&e.dispatch("execute_server")},delete_node:function(e,t){he.emit("delete_node",t)}}}),Le=o("f87c"),Me=o("85fe"),Ae=function(){var e=this,t=e.$createElement,o=e._self._c||t;return o("div",[o("div",{ref:e.chart.uuid})])},Ne=[],Pe={props:["chart"],mounted:function(){xe.a.plot(this.$refs[this.chart.uuid],this.chart.traces,this.chart.layout)},watch:{chart:{handler:function(){console.log("changed"),xe.a.newPlot(this.$refs[this.chart.uuid],this.chart.traces,this.chart.layout)},deep:!0}}},je=Pe,Ie=Object(m["a"])(je,Ae,Ne,!1,null,null,null),Re=Ie.exports;n["a"].use(ue),n["a"].component("plot",Re),n["a"].config.productionTip=!1,n["a"].use(Le["a"],he,{store:Oe}),n["a"].directive("observe-visibility",Me["a"]),new n["a"]({store:Oe,render:function(e){return e(ie)}}).$mount("#app")}});
//# sourceMappingURL=app.a95e98e2.js.map