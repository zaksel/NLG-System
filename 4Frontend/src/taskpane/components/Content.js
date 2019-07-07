import * as React from 'react';
import {Button, ButtonType, Label} from 'office-ui-fabric-react';

export default class Content extends React.Component {
    click = async () => {
        return Word.run(async context => {
          /**
           * Insert your Word code here
           */

          // insert a paragraph at the end of the document.
          const paragraph = context.document.body.insertParagraph("Hello World", Word.InsertLocation.end);

          // change the paragraph color to blue.
          paragraph.font.color = "blue";

          await context.sync();
        });
    }

    render() {
        return(
            <Button className='ms-welcome__action' iconProps={{ iconName: 'ChevronRight' }} onClick={this.click}>Generate!</Button>
        );
    }
}