import * as React from 'react';
import {Label} from 'office-ui-fabric-react';

export default class Instructions extends React.Component {
    render() {
        return(
            <div class= 'tdtg-instructions__text'>
                <Label>
                <h2>Learn how it works</h2>
                <p>
                    Enter words that are important for your text in the input field to support the Text Generator.
                    The Generator will build its sentence around these words.
                    Press TAB if you want the generator to generate the following.
                    The Text Field shows a ⚫, everywhere where Text would be inserted.
                    The length of Insertion can be set in the settings.
                </p>

                <h2>Tipps</h2>
                <p>
                    Make sure you press Save in the settings dialog!
                    Enter the First Word of the Text. The Results are better if you give a whole sentence at the beginning.
                    Keep Phrases and Words that should stay in context together and press tab after them.
                    Try giving a Headline like "Instructions" or something else that categorizes your text.
                </p>

                <h2>About the settings</h2>
                <p>
                    You can change the Language Model used by gpt-2. And also the strategy to connect your support words.
                </p>
                </Label>
            </div>
        );
    }
}