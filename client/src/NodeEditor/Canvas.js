import EventBus from '../EventBus.js'

export default class Canvas{

    constructor(container, store){
        this.container = container;
        this.graph = {};
        this.store = store;        
        this.codeNode = {};

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
        var graph = new mxGraph(this.container);  
        this.graph = graph;    
        graph.store = this.store;        

        graph.setAllowDanglingEdges(false);
        graph.setConnectable(true);
        graph.setMultigraph(true);
        graph.isCellEditable  = function(cell){return false};
        graph.htmlLabels = true;
        graph.autoSizeCells = true;
        //graph.autoSizeCellsOnAdd = true;
        graph.foldingEnabled = false;

        // Sets default styles
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
        style[mxConstants.STYLE_EDGE] = mxEdgeStyle.EntityRelation;
        style[mxConstants.STYLE_STROKEWIDTH] = '1';
        style[mxConstants.STYLE_LABEL_BACKGROUNDCOLOR] = '#FFFFFF';

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
            //Disable alt+zoom
            if (evt.altKey == true){
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

        //Adding double click event
        graph.addListener(mxEvent.DOUBLE_CLICK, (sender, evt) => {
            var cell = evt.getProperty('cell');            
            if (cell!=null){
                if (cell.isNode){
                    let code_node = this.store.state.code_nodes[cell.id];
                    this.store.dispatch('open_code_editor', code_node);
                }
            }
        });

        graph.addListener(mxEvent.MOUSE_MOVE, (sender, evt) => {
            if(graph.isMouseDown){
                console.log('yay');
            }
        });
        
        graph.addListener(mxEvent.CELLS_REMOVED, (sender, evt) => {
            var removed_cells = evt.properties.cells;
            
            console.log(evt);

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

    addNode(code_node){

        // Adds cells to the model in a single step
        var v1 = null;
        var parent = this.graph.getDefaultParent();
        this.graph.getModel().beginUpdate();
        try
        {            
            //Set cell height based on number of inputs/outputs
            var cell_height = Math.max(code_node.outputs.length, code_node.inputs.length)*30+40;            
            //var v1 = this.graph.insertVertex(parent, null, 'Node', 20, 20, 80, cell_height, 'verticalAlign=top'); 
            var v1 = this.graph.insertVertex(parent, null, code_node.display_code, 20, 20, 80, cell_height, 'verticalAlign=top'); 
            
            v1.setConnectable(false);  
            v1.isNode = true;
        }
        finally
        {
            // Updates the display
            this.graph.getModel().endUpdate();
        }

        this.changePorts(v1, code_node.outputs, 1, 'output');
        this.changePorts(v1, code_node.inputs, 0, 'input');

        return v1
    }

    changePorts(cell, port_names, position, tag){

        let model = this.graph.getModel();
        let remaining_names = [];
        let remaining_ports = [];

        var style_string = '';

        if(position == 0)
            style_string = 'labelPosition=right;align=left;deletable=0'; //Input port
        else 
            style_string = 'labelPosition=left;align=right;deletable=0'; //Output port

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

            this.graph.getView().clear(cell, false, false);
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
    }
}