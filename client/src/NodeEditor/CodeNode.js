export default class CodeNode{

    constructor(){
        this.id = '';
        this.inputs = [];
        this.outputs = [];
        this.code_source = 'local';
        this.code = '';
        this.cell_id = '';
        this.cell = {}
    }

    setCell(cell){        
        this.cell = cell
    }

    setCode(code){
        this.code = code;
        this.cell.code = code;
    }
}

/*
var parent = graph.getDefaultParent();
var model = graph.getModel();
var v1 = null;
v1 = graph.insertVertex(parent, null, label, x, y, 120, 120);
var port = graph.insertVertex(v1, null, 'Trigger', 0, 0.25, 16, 16, '', true);
*/