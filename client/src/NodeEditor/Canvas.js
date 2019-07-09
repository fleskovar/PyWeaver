import EventBus from '../EventBus.js'
import ok_icon  from '../../img/success.png'
import error_icon  from '../../img/error.png'
import calc_icon  from '../../img/hourglass.png'
import warning_icon  from '../../img/warning.png'

export default class Canvas{

    constructor(container, outline_container, store){
        this.container = container;
        this.graph = {};
        this.store = store;        
        this.codeNode = {};
        this.outline_container = outline_container;

    }

    GetModelXML(){
		let graph = this.graph;
		var enc = new mxCodec();
		var node = enc.encode(graph.getModel());
	
		var xmlString = mxUtils.getPrettyXml(node);	
		return xmlString;		
    }
    
    LoadModel(xml){
		let graph = this.graph;
        var file = xml;
        //var xmlDoc = mxUtils.load(url).getXml();
        var xmlDoc = mxUtils.parseXml(file);
        var node = xmlDoc.documentElement;
        var dec = new mxCodec(node.ownerDocument);
        dec.decode(node, graph.getModel());
	}

    mount(){
        // Disables the built-in context menu
        mxEvent.disableContextMenu(this.container);
                        
        mxGraph.prototype.isCellMovable = function(cell)
        {
            if(!this.lastEvent.altKey){
                var state = this.view.getState(cell);
                var style = (state != null) ? state.style : this.getCellStyle(cell);
                
                return this.isCellsMovable() && !this.isCellLocked(cell) && style[mxConstants.STYLE_MOVABLE] != 0;
            }
            else{
                return false;
            }
        };

        // Creates the graph inside the given container
        // Enables guides
        mxGraphHandler.prototype.guidesEnabled = true;
         // Enables snapping waypoints to terminals
        mxEdgeHandler.prototype.snapToTerminals = true;
        
        var graph = new mxGraph(this.container);  
        //var editor = new mxEditor();
        //var graph = editor.graph;
        this.graph = graph;    
        graph.store = this.store;  
        
        // Creates the outline (navigator, overview) for moving
		// around the graph in the top, right corner of the window.
		var outln = new mxOutline(graph, this.outline_container);

		// To show the images in the outline, uncomment the following code
		//outln.outline.labelsVisible = true;
		//outln.outline.setHtmlLabels(true);

        // Sets the graph container and configures the editor
        /*
        editor.setGraphContainer(this.container);
        var config = mxUtils.load(
            'editors/config/keyhandler-commons.xml').
                getDocumentElement();
        editor.configure(config);
        */

        graph.setAllowDanglingEdges(false);
        graph.setConnectable(true);
        graph.setMultigraph(true);
        
        //Only edges are editable
        graph.isCellEditable  = function(cell){
            
            return cell.edge
        };   
        
        var popupMethod = this.createPopupMenu
        graph.popupMenuHandler.factoryMethod = function(menu, cell, evt) 
        {
            return popupMethod(graph, menu, cell, evt);
        };
        
        //Only cells have html tags
        graph.isLabelMovable  = function(cell){
            
            return false
            //return cell.edge
        }; 
        
        //Only cells have html tags
        graph.isHtmlLabel  = function(cell){
            
            return !cell.edge
        };



        graph.autoSizeCells = true;
        //graph.autoSizeCellsOnAdd = true;
        //TODO: Handle autoSize on display (value) change
        graph.foldingEnabled = false;    
        graph.setPanning(true);    
        graph.scrollTileSize = new mxRectangle(0, 0, 400, 400);

        // Sets default styles   
        this.calcDefaultStyles();  
        
        var graphGetPreferredSizeForCell = graph.getPreferredSizeForCell;
        graph.getPreferredSizeForCell = function(cell)
        {
            var result = graphGetPreferredSizeForCell.apply(this, arguments);
            if(cell.edge){
                return result;
            }
            else{
                var div = document.getElementById('node_'+cell.id);

                result.width = div.offsetWidth +50;
                result.height = div.offsetHeight + 50;

                return result;
            }
        };
        
       
        /*        
        // Enables wrapping for vertex labels
        graph.isWrapping = function(cell)
        {
            return true;
        };
        
        // Enables clipping of vertex labels if no offset is defined
        graph.isLabelClipped = function(cell)
        {
            var geometry = this.model.getGeometry(cell);            
            return geometry != null && !geometry.relative
        };
        */

        /*
        var style = graph.getStylesheet().getDefaultEdgeStyle();
        style[mxConstants.STYLE_LABEL_BACKGROUNDCOLOR] = '#FFFFFF';
        style[mxConstants.STYLE_STROKEWIDTH] = '2';
        style[mxConstants.STYLE_ROUNDED] = true;
        style[mxConstants.STYLE_EDGE] = mxEdgeStyle.EntityRelation;
        */

        // Enables rubberband selection. Disable alt force.
        
        mxRubberband.prototype.isForceRubberbandEvent = function(me)
        {
	        return false;
        };
        
        new mxRubberband(graph);
        

        graph.isPort = function(cell)
        {
            var geo = this.getCellGeometry(cell);
            return false;
            //return (geo != null) ? geo.relative : false;
        };
        
        mxEvent.addMouseWheelListener(mxUtils.bind(this, function(evt, up)
        {
            //MouseScroll = zoom
            if(evt.target.localName == 'svg'){
                if(up == true)
                    graph.zoomIn();
                else graph.zoomOut();
            }	
        }));

        var keyHandler = new mxKeyHandler(graph);
        keyHandler.bindKey(46, function(evt)
        {            
            if (graph.isEnabled())
            {
                graph.removeCells();
            }
        });
        
        /*
        keyHandler.bindShiftKey(13, function(evt)
        {
            console.log('enter');
            if (graph.isEnabled())
            {                
                    console.log('add node');
            
            }
        });
        */

        //Adding new connection event
        graph.connectionHandler.addListener(mxEvent.CONNECT, (sender, evt) =>
        {
            //TODO: Create library of connection here.				
            var edge = evt.getProperty('cell');
            var data = {
                source_id: edge.source.parent.id,
                target_id: edge.target.parent.id,
                source_var: edge.source.value,
                target_var: edge.target.value,
            };
            this.store.dispatch('add_connection', data);
        });

        //Adding double click event handler
        graph.addListener(mxEvent.DOUBLE_CLICK, (sender, evt) => {
            var cell = evt.getProperty('cell'); 
            var event = evt.getProperty('event');           
            if (cell!=null && event.target.localName == 'rect'){
                if (cell.isNode){
                    let code_node = this.store.state.code_nodes[cell.id];
                    this.store.dispatch('open_code_editor', code_node);
                }
            }
        });

        graph.labelChanged = function(cell, value, evt){
            //Detects changes in labels            
            if(cell.edge){
                cell.value = value; //Changes the name of the label
                //Fires only if the label that changed was from an edge
                var data = {
                    source_id: cell.source.parent.id,
                    source_var: cell.source.value,
                    target_id: cell.target.parent.id,
                    target_var: cell.target.value,
                    name: value
                };

                //Update the edge
                this.getView().clear(cell, false, false);
                this.getView().validate();  
                this.cellSizeUpdated(cell, true);    

                this.store.dispatch('rename_connection', data);                
            }
        };

        graph.addListener(mxEvent.MOUSE_MOVE, (sender, evt) => {
            if(graph.isMouseDown){
            }
        });
        
        graph.addListener(mxEvent.CELLS_REMOVED, (sender, evt) => {
            var removed_cells = evt.properties.cells;            

            //First remove edges from graph. This ensures that referenced nodes are still registered.
            //Prevents the server from failing.
            //TODO: Add safegguarding to server side
            for(var i = 0; i < removed_cells.length; i++){
                var cell = removed_cells[i];

                if(cell.edge){
                    //Delete the connection from the graph
                    var data = {
                        source_id: cell.source.parent.id,
                        source_var: cell.source.value,
                        target_id: cell.target.parent.id,
                        target_var: cell.target.value
                    };
                    this.store.dispatch('remove_connection', data);
                }
            }

            //Once edges were removed, delete the nodes.
            for(var i = 0; i < removed_cells.length; i++){
                var cell = removed_cells[i];

                if(cell.isNode){
                    //Delete a node from the graph                
                    this.store.dispatch('delete_node', cell.id);
                }
            }
        });
    }

    addResults(results){
        var parent = this.graph.getDefaultParent();
        
        this.graph.getModel().beginUpdate();
        try
        {
            parent.results = JSON.stringify(results);
        }
        finally
        {
            // Updates the display
            this.graph.getModel().endUpdate();
        }
    }

    addScopes(scopes){
        var parent = this.graph.getDefaultParent();
        
        this.graph.getModel().beginUpdate();
        try
        {
            parent.scopes = JSON.stringify(scopes);
        }
        finally
        {
            // Updates the display
            this.graph.getModel().endUpdate();
        }
    }

    addNode(code_node){

        // Adds cells to the model in a single step
        var v1 = null;
        var parent = this.graph.getDefaultParent();
        this.graph.getModel().beginUpdate();
        try
        {            
            var outputs = code_node.outputs;
            var inputs = code_node.inputs;            

            //Takes the id of the CodeNode object.
            //If it was not set previously, this value will be null
            //and mxgraph will assign an id that will be later passed to the CodeNode object
            var id = code_node.id;

            //Set cell height based on number of inputs/outputs
            var cell_height = Math.max(outputs.length, inputs.length)*30+40;            
            
            if(!code_node.height)
                code_node.height = cell_height;

            var v1 = this.graph.insertVertex(parent, id, '', code_node.x, code_node.y, code_node.width, code_node.height, 'verticalAlign=middle'); 
            
            v1.value = "<div style='border: 1px solid;' id='node_"+v1.id+"' class='node_display'></div>"; //TODO: Find a better way to initialize the code in the node
            //TODO: Add default action code (probably should do ="")
            v1.display_act_code = '';

            v1.setConnectable(false);  
            v1.isNode = true;
        }
        finally
        {
            // Updates the display
            this.graph.getModel().endUpdate();
        }

        this.changePorts(v1, outputs, 1, 'output');
        this.changePorts(v1, inputs, 0, 'input');

        return v1
    }

    addEdge(conn_data){

        // Gets the default parent for inserting new cells. This
        // is normally the first child of the root (ie. layer 0).
        var graph = this.graph;
        var parent = graph.getDefaultParent();

        var model = graph.getModel();      
      
        var source_cell = model.cells[conn_data['source_id']];
        var source_port = null;
        for(var i = 0; i < source_cell.children.length; i++){
            let c = source_cell.children[i];
            if(c.value == conn_data['source_var']){
            source_port = c;
            break;
            }
        }

        var target_cell = model.cells[conn_data['target_id']];
        var target_port = null;
        for(var i = 0; i < target_cell.children.length; i++){
            let c = target_cell.children[i];
            if(c.value == conn_data['target_var']){
            target_port = c;
            break;
            }
        }  
                        
        // Adds cells to the model in a single step
        model.beginUpdate();
        try
        {
            var e1 = graph.insertEdge(parent, null, '', source_port, target_port);
        }
        finally
        {
            // Updates the display
            model.endUpdate();
        }
        
    }

    changePorts(cell, port_names, position, tag){
 
        let model = this.graph.getModel();
        let remaining_names = [];
        let remaining_ports = [];

        var style_string = '';

        if(position == 0)
            style_string = 'labelPosition=left;verticalLabelPosition=top;align=right;deletable=0'; //Input port
        else 
            style_string = 'labelPosition=right;verticalLabelPosition=top;align=left;deletable=0'; //Output port

        //Remove ports that are not listed in the new array
        this.graph.getModel().beginUpdate();

        try
        {  
            if(cell.children){
                for(var i =0; i < cell.children.length; i++){

                    var port = cell.children[i];
                    var port_name = port.value;       
                    var port_tag = port.tag;             

                    if(!port_names.includes(port_name) && port_tag == tag){
                        //Remove edges
                        this.graph.removeCells(model.getEdges(port), false);
                        //Remove node
                        this.graph.removeCells([port], false);
                        i -= 1;
                    }else{
                        if(port_tag == tag){
                            remaining_ports.push(port);
                            remaining_names.push(port_name);
                        }
                    }           
                }
            }
            //Add remaining nodes
            for(var i =0; i < port_names.length; i++){
                
                var port_name = port_names[i];

                if(!remaining_names.includes(port_name)){
                    var p = this.graph.insertVertex(cell, null, port_name, position, 1.0/(port_names.length+1) * (i+1), 10, 10, style_string, true); 
                    p.geometry.offset = new mxPoint(-5, -5);
                    p.setConnectable(true);  
                    p.tag = tag;                  
                }else{                    
                    var p = remaining_ports[i];
                    p.geometry.y = 1.0/(port_names.length+1) * (i+1);
                }            
            }

            //This appears to clear the cell's content (but it shouldnt)
            //this.graph.getView().clear(cell, false, false);
            this.graph.getView().validate();

        }
        finally
        {
            // Updates the display            
            this.graph.getModel().endUpdate();
        }
    }

    updateCell(cell){
        this.graph.getView().clear(cell, false, false);
        this.graph.getView().validate();  
        this.graph.cellSizeUpdated(cell, true);      
    }

    updateCellSize(cell){        
        this.graph.cellSizeUpdated(cell, true);      
    }

    setCellColor(color){
        var cells = this.graph.selectionModel.cells;

        for(var i = 0; i < cells.length; i++){
            var cell = cells[i];
            var style = cell.getStyle();

            var newStyle=mxUtils.setStyle(style,mxConstants.STYLE_STROKECOLOR, color);
            this.graph.setCellStyle(newStyle,[cell]);
        }
    }

    setCellStroke(size){
        var cells = this.graph.selectionModel.cells;
        
        for(var i = 0; i < cells.length; i++){
            var cell = cells[i];
            var style = cell.getStyle();

            var newStyle=mxUtils.setStyle(style,mxConstants.STYLE_STROKEWIDTH, size);
            this.graph.setCellStyle(newStyle,[cell]);
        }  

    }

    setDashed(is_dashed){

        var val = 0
        var cells = this.graph.selectionModel.cells;
        
        for(var i = 0; i < cells.length; i++){
            var cell = cells[i];
            var style = cell.getStyle();

            if(is_dashed)
                val = 1;
            
            var newStyle=mxUtils.setStyle(style,mxConstants.STYLE_DASHED, val);
            this.graph.setCellStyle(newStyle,[cell]);
        }
    }

    calcDefaultStyles(){

        let graph = this.graph;
        //Dark mode
        if(this.store.state.config.dark_mode){
            var style = graph.getStylesheet().getDefaultVertexStyle();
            style['fillColor'] = '#212121';
            style['strokeColor'] = '#FFFFFF';
            style['fontColor'] = '#FFFFFF';
            style['fontStyle'] = '1';

            style = graph.getStylesheet().getDefaultEdgeStyle();
            style['strokeColor'] = '#FFFFFF';
            style['fontColor'] = '#FFFFFF';
            style['fontStyle'] = '0';
            style['fontStyle'] = '0';
            style['startSize'] = '8';
            style['endSize'] = '8';
            style[mxConstants.STYLE_ROUNDED] = true;
            style[mxConstants.STYLE_EDGE] = mxEdgeStyle.OrthConnector;
            style[mxConstants.STYLE_STROKEWIDTH] = '1';
            style[mxConstants.STYLE_LABEL_BACKGROUNDCOLOR] = '#212121';
        }
        else{
            //Light mode
            
            var style = graph.getStylesheet().getDefaultVertexStyle();
            style['fillColor'] = '#FFFFFF';
            style['strokeColor'] = '#000000';
            style['fontColor'] = '#000000';
            style['fontStyle'] = '1';
            
            style = graph.getStylesheet().getDefaultEdgeStyle();
            style['strokeColor'] = '#000000';
            style['fontColor'] = '#000000';
            style['fontStyle'] = '0';
            style['fontStyle'] = '0';
            style['startSize'] = '8';
            style['endSize'] = '8';
            style[mxConstants.STYLE_ROUNDED] = true;
            style[mxConstants.STYLE_EDGE] = mxEdgeStyle.OrthConnector;
            style[mxConstants.STYLE_STROKEWIDTH] = '1';
            style[mxConstants.STYLE_LABEL_BACKGROUNDCOLOR] = '#FFFFFF';            
        }
    }

    updateSyles(){
        this.calcDefaultStyles();
    }

    setOverlay(cell, overlay_name){

        var img = null;
        var tooltip_text = ''

        if(overlay_name == 'ok')
        {
            tooltip_text = 'Calculation succeeded';
            img = new mxImage(ok_icon, 16, 16);
            
        }
        else if (overlay_name == 'error')
        {
            tooltip_text = 'Error';
            img = new mxImage(error_icon, 16, 16);            
        }
        else if (overlay_name == 'warning')
        {
            tooltip_text = 'Not enough inputs';
            img = new mxImage(warning_icon, 16, 16);            
        }
        else{
            tooltip_text = 'Executing...';
            img = new mxImage(calc_icon, 16, 16);            
        }
        var overlay = new mxCellOverlay(img, tooltip_text);
        this.graph.addCellOverlay(cell, overlay);
    }

    removeOverlay(cell){
        this.graph.removeCellOverlays(cell);
    }

    createPopupMenu(graph, menu, cell, evt)
    {        
        if (cell != null)
        {
            menu.addItem('Cell Item', 'editors/images/image.gif', function()
            {
                //mxUtils.alert('MenuItem1');
                window.open( 'http://localhost:8080/node_viewer.html', 'name', 'location=no,scrollbars=yes,status=no,toolbar=yes,resizable=yes');
            });
        }
        else
        {
            /*
            menu.addItem('No-Cell Item', 'editors/images/image.gif', function()
            {
                mxUtils.alert('MenuItem2');
            });
            */
        }
        /*
        menu.addSeparator();
        menu.addItem('MenuItem3', '../src/images/warning.gif', function()
        {
            mxUtils.alert('MenuItem3: '+graph.getSelectionCount()+' selected');
        });
        */
    };

}