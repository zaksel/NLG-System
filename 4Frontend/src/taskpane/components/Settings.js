import * as React from 'react';
import {Label, Dropdown, SpinButton, PrimaryButton} from 'office-ui-fabric-react';

let set_var = {
    strategy: 's3',
    model: '117M',
    language: 'de',
    len: 5,
    seed: 0,
    top_k: 40,
    beam_width: 20,
    beam_depth: 5,
    scope: 6,
    timeout: "None"
};

export default class Settings extends React.Component {
    constructor() {
        super();
        this.state = {top_k: true, beam_width: false, beam_depth: false, scope: false, timeout: false};
        this.change_view = this.change_view.bind(this);
    }

    change_view(strategy) {
        set_var.strategy = strategy;
        if (strategy === "s1a") {
            this.setState({top_k: false, beam_width: true, beam_depth: true, scope: false, timeout: true});
        }
        if (strategy === "s1b") {
            this.setState({top_k: false, beam_width: true, beam_depth: true, scope: true, timeout: true});
        }
        if (strategy === "s2") {
            this.setState({top_k: true, beam_width: false, beam_depth: false, scope: false, timeout: true});
        }
        if (strategy === ("s3" || "s4")) {
            this.setState({top_k: true, beam_width: false, beam_depth: false, scope: false, timeout: false});
        }


    }

    render() {
        return (
            <div className='tdtg-settings__elements'>
                <p><Dropdown id='strategy' label="Choose a Strategy" onChanged={option => this.change_view(option.key)}
                             options={[{key: 's1a', text: 'Beam-Search'}, {
                                 key: 's1b',
                                 text: 'Beam-Search (Scope)'
                             }, {key: 's2', text: 'Search until fit'}, {
                                 key: 's3',
                                 text: 'Cut-off and Insert'
                             }, {key: 's4', text: 'BERT-GPT2 Hybrid'}]}
                             defaultSelectedKey={set_var.strategy}/></p>
                <p><Dropdown id='model' label="Choose a language model" onChanged={(option) => {
                    set_var.model = option.key
                }}
                             options={[{key: '117M', text: '117M'}, {key: 'ISW_Model', text: 'ISW_Model'}]}
                             defaultSelectedKey={set_var.model}/></p>
                <p><Dropdown id='language' label="Output language" onChanged={(option) => {
                    set_var.language = option.key
                }}
                             options={[{key: 'None', text: 'None'}, {key: 'en', text: 'en'}, {
                                 key: 'de',
                                 text: 'de'
                             }, {key: 'fra', text: 'fra'}]}
                             defaultSelectedKey={set_var.language}/></p>
                <p><SpinButton id='len' label={'length:'}
                               styles={{label: {width: 100}}}
                               defaultValue={set_var.len}
                               onIncrement={(value) => {
                                   value = parseInt(value);
                                   if (value < 250) {
                                       value = value + 1;
                                       set_var.len = value;
                                       return value
                                   }
                               }}
                               onDecrement={(value) => {
                                   value = parseInt(value);
                                   if (value > 1) {
                                       value = value - 1;
                                       set_var.len = value;
                                       return value
                                   }
                               }}
                               onValidate={(value) => {
                                   set_var.len = value;
                                   return value
                               }}/></p>
                <p><SpinButton id='seed' label={'seed:'}
                               styles={{label: {width: 100}}}
                               defaultValue={set_var.seed}
                               onIncrement={(value) => {
                                   if (value === "None") {
                                       set_var.seed = 0;
                                       return "0"
                                   }
                                   if (value === "0") {
                                       set_var.seed = 1;
                                       return 1
                                   }
                                   value = value + 1;
                                   set_var.seed = value;
                                   return value;
                               }}
                               onDecrement={(value) => {
                                   if (value === "0") {
                                       set_var.seed = "None";
                                       return "None"
                                   }
                                   if (value == 1) {
                                       set_var.seed = 0;
                                       return "0"
                                   }
                                   parseInt(value);
                                   value = value - 1;
                                   set_var.seed = value;
                                   return (value);
                               }}
                               onValidate={(value) => {
                                   if ((value % 1 == 0 && value > 0) || value === "None") {
                                       set_var.seed = value;
                                       return value
                                   }
                                   return set_var.seed
                               }}/></p>
                <p><SpinButton id='top_k' label='top_k:'
                               styles={{label: {width: 100}}}
                               defaultValue={set_var.top_k}
                               disabled={!this.state.top_k}
                               onIncrement={(value) => {
                                   value = parseInt(value);
                                   value = value + 1;
                                   set_var.top_k = value;
                                   return value;
                               }}
                               onDecrement={(value) => {
                                   value = parseInt(value);
                                   if (value > 0) {
                                       value = value - 1;
                                       set_var.top_k = value
                                   }
                                   return value;
                               }}
                               onValidate={(value) => {
                                   if (value % 1 === 0 && value > 0) {
                                       set_var.top_k = value;
                                       return value
                                   }
                                   return set_var.top_k
                               }}/></p>
                <p><SpinButton ref='beam_width' label='beam-width:'
                               styles={{label: {width: 100}}}
                               defaultValue={set_var.beam_width}
                               disabled={!this.state.beam_width}
                               onIncrement={(value) => {
                                   value = parseInt(value);
                                   value = value + 1;
                                   set_var.beam_width = value;
                                   return value;
                               }}
                               onDecrement={(value) => {
                                   value = parseInt(value);
                                   if (value > 0) {
                                       value = value - 1;
                                       set_var.beam_width = value
                                   }
                                   return value;
                               }}
                               onValidate={(value) => {
                                   if (value % 1 === 0 && value > 0) {
                                       set_var.beam_width = value;
                                       return value
                                   }
                                   return set_var.beam_width
                               }}/></p>
                <p><SpinButton id='beam_depth' label='beam-depth:'
                               styles={{label: {width: 100}}}
                               defaultValue={set_var.beam_depth}
                               disabled={!this.state.beam_depth}
                               onIncrement={(value) => {
                                   value = parseInt(value);
                                   value = value + 1;
                                   set_var.beam_depth = value;
                                   return value;
                               }}
                               onDecrement={(value) => {
                                   value = parseInt(value);
                                   if (value > 0) {
                                       value = value - 1;
                                       set_var.beam_depth = value
                                   }
                                   return value;
                               }}
                               onValidate={(value) => {
                                   if (value % 1 === 0 && value > 0) {
                                       set_var.beam_depth = value;
                                       return value
                                   }
                                   return set_var.beam_depth
                               }}/></p>
                <p><SpinButton id='scope' label='scope:'
                               styles={{label: {width: 100}}}
                               defaultValue={set_var.scope}
                               disabled={!this.state.scope}
                               onIncrement={(value) => {
                                   value = parseInt(value);
                                   value = value + 1;
                                   set_var.scope = value;
                                   return value;
                               }}
                               onDecrement={(value) => {
                                   value = parseInt(value);
                                   if (value > 0) {
                                       value = value - 1;
                                       set_var.scope = value
                                   }
                                   return value;
                               }}
                               onValidate={(value) => {
                                   if (value % 1 === 0 && value > 0) {
                                       set_var.scope = value;
                                       return value
                                   }
                                   return set_var.scope
                               }}/></p>
                <p><SpinButton id='timeout' label='timeout (in s):'
                               styles={{label: {width: 100}}}
                               defaultValue={set_var.timeout}
                               disabled={!this.state.timeout}
                               onIncrement={(value) => {
                                   if (value === "None") {
                                       set_var.timeout = 10;
                                       return 10
                                   }
                                   value = parseInt(value);
                                   value = value + 10;
                                   set_var.timeout = value;
                                   return value;
                               }}
                               onDecrement={(value) => {
                                   value = parseInt(value);
                                   if (value == 10) {
                                       set_var.timeout = "None";
                                       return "None"
                                   } else {
                                       value = value - 10;
                                       set_var.timeout = value
                                   }
                                   return value;
                               }}
                               onValidate={(value) => {
                                   if ((value % 10 === 0 && value > 0) || value === "None") {
                                       set_var.timeout = value;
                                       return value
                                   }
                                   return set_var.timeout
                               }}/></p>
            </div>
        );
    }
}

export {set_var};