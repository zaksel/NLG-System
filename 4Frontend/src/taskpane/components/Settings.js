import * as React from 'react';
import {Label, Dropdown, SpinButton, PrimaryButton} from 'office-ui-fabric-react';

let settings = {
    model: '117M',
    language: 'de',
    len: "5",
    seed: "0",
    temp: "1.0",
    top_p: "0.9"
};

export default class Settings extends React.Component {

    save = async () => {
        //send settings to backend
        $.ajax({
            type: "POST",
            url: "http://127.0.0.1:5000/settings",
            data: JSON.stringify(settings),
            dataType: 'json',
            success: function () {
                console.log("saved settings")
            }
        });
    };

    render() {
        return (
            <div className='tdtg-settings__elements'>
                <Dropdown id='model' label="Choose a languagemodel" onChanged={(option) => {settings.model = option.key}}
                          options={[{key: '117M', text: '117M'}, {key: '345M', text: '345M'}, {
                              key: 'ISW_Model',
                              text: 'ISW_Model'
                          }]}
                          defaultSelectedKey={settings.model}/>
                <Dropdown id='language' label="Output language" onChanged={(option) => {settings.language = option.key}}
                          options={[{key: 'en', text: 'en'}, {key: 'de', text: 'de'}, {key: 'fra', text: 'fra'}]}
                          defaultSelectedKey={settings.language}/>
                <SpinButton id='len' label={'Avg. Distance between support words:'}
                            defaultValue={settings.len}
                            onIncrement={(value) => {
                                value = parseInt(value);
                                if (value < 250){
                                    value = value + 1;
                                    settings.len = value;
                                    return value
                                }
                            }}
                            onDecrement={(value) => {
                                value = parseInt(value);
                                if (value > 1){
                                    value = value - 1;
                                    settings.len = value;
                                    return value
                                }
                            }}
                            onValidate={(value) => {
                                settings.len = value;
                                return value
                            }}/>
                <SpinButton id='seed' label={'Seed for random generations (0 is None):'}
                            defaultValue={settings.seed}
                            onIncrement={(value) => {
                                value = parseInt(value);
                                if (value < 250){
                                    value = value + 1;
                                    settings.seed = value;
                                    return value
                                }
                            }}
                            onDecrement={(value) => {
                                value = parseInt(value);
                                if (value > 0){
                                    value = value - 1;
                                    settings.seed = value;
                                    return value
                                }
                            }}
                            onValidate={(value) => {
                                settings.seed = value;
                                return value
                            }}/>
                <SpinButton id='temp' label={'Temperature in boltzmann distribution:'}
                            defaultValue={settings.temp}
                            onIncrement={(value) => {
                                value = parseFloat(value);
                                if (value < 1.0){
                                    value = value + 0.1;
                                    value = value.toFixed(1);
                                    settings.temp = value}
                                return value;
                            }}
                            onDecrement={(value) => {
                                value = parseFloat(value);
                                if (value > 0){
                                    value = value - 0.1;
                                    value = value.toFixed(1);
                                    settings.temp = value}
                                return value;
                            }}
                            onValidate={(value) => {
                                settings.temp = value;
                                return value
                            }}/>
                <SpinButton id='top_p' label={'top_p for nucleus sampling (overwrites top_k):'}
                            defaultValue={settings.top_p}
                            onIncrement={(value) => {
                                value = parseFloat(value);
                                if (value < 1.0){
                                    value = value + 0.1;
                                    value = value.toFixed(1);
                                    settings.top_p = value}
                                return value;
                            }}
                            onDecrement={(value) => {
                                value = parseFloat(value);
                                if (value > 0){
                                    value = value - 0.1;
                                    value = value.toFixed(1);
                                    settings.top_p = value}
                                return value;
                            }}
                            onValidate={(value) => {
                                settings.top_p = value;
                                return value
                            }}/>
                <Label/>
                <PrimaryButton className='tdtg-content__button' id='button' iconProps={{iconName: 'ChevronRight'}}
                        onClick={this.save}>Save Settings</PrimaryButton>
            </div>
        );
    }
}