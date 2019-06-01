import DisplayConstants from '../Constants.js'


export default class CodeNode{

    constructor(default_display, canvas, store, id = null){
        this.canvas = canvas;

        if(id)
            this.id = id;
        else this.id = null;

        this.inputs = {};
        this.outputs = {};
        this.code_source = 'local';
        this.code = '';
        this.display_code = default_display;
        this.display_act_code = '';
        this.cell_id = '';
        this.cell = {}
        this.compiled_display_code = '';
        this.compileDisplayCode();
        this.store = store;

        this.x = 20;
        this.y = 20;
        this.width = 100;
        this.height = null;
    }

    setCell(cell){        
        this.cell = cell;
        this.id = cell.id;
    }

    compileDisplayCode(){
        //The idea behind this is to wrapp the display code with a div which we can track easily.
        //We then use the 'node' attribute to know which node/cell owns this code
        //Then, before sending the "excute" event to the server, we should gather all the inputs and
        //pass them to the server so that they can be injected to each node
        this.compiled_display_code = 
        "<div "+DisplayConstants.DISPLAY_NODE_ID_ATTR+"='"+this.cell.id+"' class='"+DisplayConstants.DISPLAY_CLASS+"'id='node_"+this.cell.id+"'>"+
        this.display_code +
        "</div>";        
    }

    setCode(code){
        this.code = code;
        this.cell.code = code;
    }

    setDisplayCode(code){
        this.display_code = code;
        this.compileDisplayCode();
        //this.cell.value = this.compiled_display_code;
        this.cell.display_code = code;
        //this.canvas.updateCell(this.cell);
    }

    setDisplayActCode(code){
        this.display_act_code = code;
        this.cell.display_act_code = code;
    }
}