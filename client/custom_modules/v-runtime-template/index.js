import {Val} from '../../src/directives/InitDirective.js'
import Plotly from 'plotly.js-dist';


const getKeysFromOptions = options => [
  ...Object.keys((options.data && options.data()) || {}),
  ...Object.keys(options.props || {})
];

const defineDescriptor = (src, dest, name) => {
  if (!dest.hasOwnProperty(name)) {
    const descriptor = Object.getOwnPropertyDescriptor(src, name);
    Object.defineProperty(dest, name, descriptor);
  }
};

const merge = objs => {
  const res = {};
  objs.forEach(obj => {
    obj &&
      Object.getOwnPropertyNames(obj).forEach(name =>
        defineDescriptor(obj, res, name)
      );
  });
  return res;
};

const buildFromProps = (obj, props) => {
  const res = {};
  props.forEach(prop => defineDescriptor(obj, res, prop));
  return res;
};

export default {
  props: {
    template: String,
    display_code: String
  },
  directives:{
    Val
  },
  data(){
    return {
      plotly: Plotly,
    };
  },
  render(h) {
    console.log("rendering");
    if (this.template) {
      const { $data, $props, $options } = this.$parent;

      var disp_code = '{}';
      if(this.display_code)
        disp_code = this.display_code;

      //Update functions only if display code changed
      if(disp_code != this.$parent.$data._previous_display_code){
        //If the display code changed, delete the previous injected functions
        var embedded_x = 'function(){return '+this.$parent.$data._previous_display_code+' }();';
        var previousActionFunctions = Function("return " + embedded_x)();
        
        //Iterate and delete the functions
        for(var f in previousActionFunctions){        
          delete $options.methods[f];
          delete this.$parent[f];;
        };

        this.$parent.$data._previous_display_code = disp_code; //Backup last code
        
        embedded_x = 'function(){return '+disp_code+' }();';
        var actionFunctions = Function("return " + embedded_x)();     

        //Inject methods into parent scope
        for(var f in actionFunctions){
          var boundFunc = actionFunctions[f].bind(this.$parent);        
          //$options.methods[f] = actionFunctions[f];
          //this.$parent[f] = actionFunctions[f];

          $options.methods[f] = boundFunc;
          this.$parent[f] = boundFunc;
        };
      }
      
      if(this.$parent.$data._previous_template != this.template)
      {
        this.$parent.$data.scope = {};
        this.$parent.$data._previous_template = this.template;
      }

      const methodKeys = Object.keys($options.methods || {});
      const allKeys = getKeysFromOptions($options).concat(methodKeys);
      const methods = buildFromProps(this.$parent, methodKeys);
      const props = merge([$data, $props, methods]);

      const dynamic = {
        template: this.template || "<div></div>",
        props: allKeys,
        computed: $options.computed,
        components: $options.components
      };

      return h(dynamic, {
        props
      });
    }
  }
};
