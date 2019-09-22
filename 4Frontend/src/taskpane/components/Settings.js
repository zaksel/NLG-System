import * as React from 'react';
import {Label, Dropdown, SpinButton, PrimaryButton} from 'office-ui-fabric-react';

let set_var = {
    strategy: 's3',
    model: '117M',
    language: null,
    len: 5,
    seed: 0,
    top_k: 40,
    beam_width: 20,
    beam_depth: 5,
    scope: 6,
    timeout: 120
};

let views = {
    s1a: {model: false, language: false, len: false, top_k: false, beam_width: true, beam_depth: true, scope: false, timeout: true},
    s1b: {model: false, language: false, len: false, top_k: false, beam_width: true, beam_depth: true, scope: true, timeout: true},
    s2: {model: true, language: false, len: true, top_k: true, beam_width: false, beam_depth: false, scope: false, timeout: true},
    s34: {model: true, language: true, len: true, top_k: true, beam_width: false, beam_depth: false, scope: false, timeout: false}
};

export default class Settings extends React.Component {
    constructor() {
        super(self);
        if (set_var.strategy === "s1a") {this.state = views.s1a;}
        if (set_var.strategy === "s1b") {this.state = views.s1b;}
        if (set_var.strategy === "s2") {this.state = views.s2;}
        if (set_var.strategy === "s3" || set_var.strategy === "s4") {this.state = views.s34;}
        this.change_view = this.change_view.bind(this);
    }

    change_view(strategy) {
        set_var.strategy = strategy;
        if (strategy === "s1a") {this.setState(views.s1a);}
        if (strategy === "s1b") {this.setState(views.s1b);}
        if (strategy === "s2") {this.setState(views.s2);}
        if (strategy === "s3" || strategy === "s4") {this.setState(views.s34);}
    }

    render() {
        return (
            <div className='tdtg-settings__elements'>
                <p><Dropdown id='strategy' label="Choose a Strategy" onChanged={option => this.change_view(option.key)}
                             options={[
                                 {key: 's1a', text: 'Beam-Search'},
                                 {key: 's1b', text: 'Beam-Search (Scope)'},
                                 {key: 's2', text: 'Search until fit'},
                                 {key: 's3', text: 'Cut-off and Insert'},
                                 {key: 's4', text: 'BERT-GPT2 Hybrid'}
                                 ]}
                             defaultSelectedKey={set_var.strategy}/></p>
                <p><Dropdown id='model' label="Choose a language model"
                             onChanged={(option) => {set_var.model = option.key}}
                             options={[{key: '117M', text: '117M'}, {key: 'ISW_Model', text: 'ISW_Model'}]}
                             defaultSelectedKey={set_var.model}
                             disabled={!this.state.model}/></p>
                <p><Dropdown id='language' label="Output language"
                             onChanged={(option) => {set_var.language = option.key}}
                             options={[{key: null, text: 'No Translation'},
                                 {key: 'en', text: 'en'},
                                 {key: 'de', text: 'de'},
                                 {key: 'fr', text: 'fr'}]}
                             defaultSelectedKey={set_var.language}
                             disabled={!this.state.language}/></p>
                <p><SpinButton id='len' label={'length:'}
                               styles={{label: {width: 100}}}
                               disabled={!this.state.len}
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
                                   set_var.len = parseInt(value);
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
                                       set_var.seed = null;
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
                                       set_var.seed = parseInt(value);
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
                                       set_var.top_k = parseInt(value);
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
                                       set_var.beam_width = parseInt(value);
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
                                       set_var.beam_depth = parseInt(value);
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
                                       set_var.scope = parseInt(value);
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
                                       set_var.timeout = null;
                                       return "None"
                                   } else {
                                       value = value - 10;
                                       set_var.timeout = parseInt(value);
                                   }
                                   return value;
                               }}
                               onValidate={(value) => {
                                   if ((value % 10 === 0 && value > 0) || value === "None") {
                                       set_var.timeout = parseInt(value);
                                       return value
                                   }
                                   return set_var.timeout
                               }}/></p>
            </div>
        );
    }
}

export {set_var};