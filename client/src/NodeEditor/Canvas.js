import EventBus from '../EventBus.js'
import * as mxgraph from 'mxgraph';

const {
	mxClient, mxGraph, mxRubberband, mxUtils, mxEvent, mxPoint, mxConstants, mxEdgeStyle, mxKeyHandler
} = mxgraph();


export default class Canvas{

    constructor(container, store){
        this.container = container;
        this.graph = {};
        this.store = store;        
        this.codeNode = {};
    }

    mount(){
        // Disables the built-in context menu
        mxEvent.disableContextMenu(this.container);
                        
        // Creates the graph inside the given container
        var graph = new mxGraph(this.container);  
        this.graph = graph;    
        graph.store = this.store;        

        graph.setAllowDanglingEdges(false);
        graph.setConnectable(true);
        graph.setMultigraph(true);
        graph.isCellEditable  = function(cell){return false};

        var style = graph.getStylesheet().getDefaultEdgeStyle();
        style[mxConstants.STYLE_LABEL_BACKGROUNDCOLOR] = '#FFFFFF';
        style[mxConstants.STYLE_STROKEWIDTH] = '2';
        style[mxConstants.STYLE_ROUNDED] = true;
        style[mxConstants.STYLE_EDGE] = mxEdgeStyle.EntityRelation;

        // Enables rubberband selection
        new mxRubberband(graph);

        graph.isPort = function(cell)
        {
            var geo = this.getCellGeometry(cell);
            return false;
            //return (geo != null) ? geo.relative : false;
        };
        
        mxEvent.addMouseWheelListener(mxUtils.bind(this, function(evt, up)
        {
            //if (evt.altKey == true){
                if(up == true)
                    graph.zoomIn();
                else graph.zoomOut();

            //}	
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
                    this.store.dispatch('open_code_editor', cell.codeNode);
                }
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
                        source_var: cell.source.value
                    };
                    this.store.dispatch('remove_connection', data);
                }
            }

            //Once edges were removed, delete the nodes.
            for(var i = 0; i < removed_cells.length; i++){
                var cell = removed_cells[i];

                if(cell.isNode){
                    //Delete a node from the graph
                
                this.store.dispatch('add_connection', data);
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
            var v1 = this.graph.insertVertex(parent, null, 'Node', 20, 20, 80, cell_height, 'verticalAlign=top'); 
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
}