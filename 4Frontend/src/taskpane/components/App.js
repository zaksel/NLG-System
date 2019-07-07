import * as React from 'react';
import {Label, Pivot, PivotItem, PivotLinkFormat, PivotLinkSize} from 'office-ui-fabric-react';

import Content from './Content';
import Settings from './Settings';
import Instructions from './Instructions';
import About from './About';

export default class App extends React.Component {
  render() {
    return (
      <div className='ms-welcome'>
        <Pivot linkFormat={PivotLinkFormat.links} linkSize={PivotLinkSize.normal}>
          <PivotItem headerText="Inputs">
            <Content/>
          </PivotItem>
          <PivotItem headerText="Settings">
            <Settings/>
          </PivotItem>
          <PivotItem headerText="Instructions">
            <Label>Learn how it works</Label>
            <Instructions/>
          </PivotItem>
          <PivotItem headerText="About">
            <About title="TDTG" logo="./assets/logo-filled.png" message="Technical Document Text Generator was created by Hannes-Christopher Zakes at ISW (Institut für Steuerungstechnik Universität Stuttgart)"/>
          </PivotItem>
        </Pivot>
      </div>
    );
  }
}
