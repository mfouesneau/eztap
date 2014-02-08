from bottle import route, request
from static_routes import *
from htmlhelpers import *
from config import __WEBSERVER__, __author__, __version__


def Catalog_block():
    txt = html_div(html_div("""
    <label for="Name">
      Catalog:
       <input id="catName" type="text" required="" placeholder="http://....", role="textbox" style="width:90%;" aria-autocomplete="both" >
    </label>
    """, 'style="margin:5px;width: 100%;"')
    + html_div(html_list( [
        'Tablename: <label id="catId"> N/A </label>',
        #'URL: <label id="catId"> N/A </label>',
        'Description: <label id="catDesc"> N/A </label>',
        'Number of entries: <label id="nRows"></label>'
        ]),'style="margin:15px;width: 100%;"' )
    )

    txt +=  html_div( """
                <div id="tabMetaCaption">
                   <!--a href="#">Column selection</a></h3-->
                   <span><b>Column selection</b></span>
                                   <a href=""><img src="img/sort_desc.png" alt="rolllup" title="Show/hide columns metadata"></a>
                </div>
                <div id="tabMetaToggleDiv" style="display: none;">
                                <table cellpadding="0" cellspacing="0" border="0" class="display" id="tab_meta">
                                <thead>
                                   <tr>
                                      <th width="4%"><input type="checkbox" id="allMetaCheckbox" checked="checked"></th>
                                      <th width="20%">ColName</th>
                                      <th width="8%">Type</th>
                                      <th width="10%">Fmt</th>
                                      <th width="10%">Unit</th>
                                      <th width="40%">Description</th>
                                      <th width="40%">Null</th>

                                   </tr>
                                 </thead>
                                    <tbody>
                                        <tr class="odd">
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                        </tr>
                                        <tr tr="" class="even">
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                            <td>&nbsp;</td>
                                        </tr>
                                    </tbody>
                                </table>
                </div>
                """
            , 'id="tabMeta"')
    txt = block(txt, 'Catalog', id="queryForm")
    return txt


def Sky_block():
    Conehtml_div = """
    <label for="radioConeSearch">
        <input type="radio" id="radioConeSearch" name="skyAreaRadio">
        Cone search
    </label>"""
    Conehtml_div += html_div("""
              <ul class="radioOptions">
                 <li class="radioOptions">
                    <label for="optionConeSearchCenter" disabled="disabled"> Center: </label>
                    <input type="text" id="optionConeSearchCenter" placeholder="Position/Object name" disabled="disabled">
                 </li>
                 <li class="radioOptions">
                    <label for="optionConeSearchRadius" disabled="disabled"> Radius: </label>
                    <input style="width:90px;" type="number" step="1" min="0" max="3600" value="5" id="optionConeSearchRadius" disabled="disabled">
                    <select id="distUnitSelect" disabled="disabled">
                       <option value="mas">mas</option>
                       <option value="arcsec" selected="selected">arcsec</option>
                       <option value="arcmin">arcmin</option>
                       <option value="deg">deg</option>
                    </select>
                 </li>
              </ul>""", "id=optionConeSearch")

    Boxhtml_div = """
            <label for="radioBox">
            <input type="radio" id="radioBox" name="skyAreaRadio">
        Centered Box
        </label> """
    Boxhtml_div += html_div( """
               <ul class="radioOptions">
                  <li class="radioOptions">
                     <label for="optionBoxCenter" disabled="disabled"> Center: </label>
                     <input type="text" id="optionBoxCenter" placeholder="Position/Object name" disabled="disabled">
                  </li>
                  <li class="radioOptions">
                     <label for="optionBoxWidth" disabled="disabled"> Width: </label>
                     <input style="width:90px;" type="number" step="1" min="0" max="36000" value="20" id="optionBoxWidth" disabled="disabled">
                     <select id="boxWidthUnitSelect" disabled="disabled">
                             <option value="mas">mas</option>
                             <option value="arcsec" selected="selected">arcsec</option>
                             <option value="arcmin">arcmin</option>
                             <option value="deg">deg</option>
                     </select>
                  </li>
                  <li class="radioOptions">
                     <label for="optionBoxHeight" disabled="disabled"> Height: </label>
                     <input style="width:90px;" type="number" step="1" min="0" max="36000" value="10" id="optionBoxHeight" disabled="disabled">
                     <select id="boxHeightUnitSelect" disabled="disabled">
                        <option value="mas">mas</option>
                        <option value="arcsec" selected="selected">arcsec</option>
                        <option value="arcmin">arcmin</option>
                        <option value="deg">deg</option>
                     </select>
                  </li>
                  <li class="radioOptions">
                    <label for="optionBoxPA" disabled="disabled"> <span title="Angle between the North axis and the Height axis, looking at the unit sphere from the exterior." class="tooltip">Angle</span>: </label>
                    <input style="width:90px;" type="number" step="1" min="-90" max="90" value="0" id="optionBoxPA" disabled="disabled">
                    <select id="boxPAUnitSelect" disabled="disabled">
                       <option value="deg" selected="selected">deg</option>
                    </select>
                 </li>
              </ul>
          """, "id = optionBox")

    Rectanglehtml_div = """
        <label for="radioZone">
       <input type="radio" id="radioZone" name="skyAreaRadio">
       Rectangle
    </label> """
    Rectanglehtml_div += html_div("""
           <ul class="radioOptions">
              <li class="radioOptions">
                 <label for="optionZoneRaMin" disabled="disabled"> Ra <sub>min</sub>: </label>
                 <input style="width:90px;" type="number" step="0.00001" min="0" max="360" value="350" id="optionZoneRaMin" disabled="disabled">
                 <label for="optionZoneRaMax" disabled="disabled"> RA<sub>max</sub>: </label>
                 <input style="width:90px;" type="number" step="0.00001" min="0" max="360" value="20" id="optionZoneRaMax" disabled="disabled">
              </li>
              <li class="radioOptions">
                 <label for="optionZoneDecMin" disabled="disabled">
            Dec<sub>min</sub>:
         </label>
                 <input style="width:90px;" type="number" step="0.00001" min="-90" max="90" value="-45" id="optionZoneDecMin" disabled="disabled">
                 <label for="optionZoneDecMax" disabled="disabled">
            Dec<sub>max</sub>:
        </label>
                 <input style="width:90px;" type="number" step="0.00001" min="-90" max="90" value="-30" id="optionZoneDecMax" disabled="disabled">
             </li>
          </ul> """, 'id="optionZone"')

    HealPixhtml_div = """
        <label for="radioHealpixIdx">
       <input type="radio" id="radioHealpixIdx" name="skyAreaRadio">
       Healpix cell (ICRS)
    </label> """

    HealPixhtml_div += html_div("""
        <div id="optionHealpixCell">
           <ul class="radioOptions">
             <li class="radioOptions">
                <label for="optionHealpixNside" disabled="disabled"> Nside: </label>
                <select id="optionHealpixNside" disabled="disabled">
                   <option value="1">1</option>
                   <option value="2">2</option>
                   <option value="4">4</option>
                   <option value="8">8</option>
                   <option value="16">16</option>
                   <option value="32">32</option>
                   <option value="64">64</option>
                   <option value="128">128</option>
                   <option value="256">256</option>
                   <option value="512" selected="selected">512</option>
                   <option value="1024">1024</option>
                   <option value="2048">2048</option>
                </select>
             </li>
             <li class="radioOptions">
                <label for="optionHealpixIdx" disabled="disabled">Index: </label>
                <input type="number" step="1" min="0" max="47" value="0" id="optionHealpixIdx" disabled="disabled">
             </li>
          </ul>""", "id=optionHealpixCell")
    AllSkyhtml_div = """
        <label for="radioAllSky">
               <input type="radio" id="radioAllSky" name="skyAreaRadio" checked="checked">
           All-sky
        </label><br> """
    txt1 = html_div(AllSkyhtml_div+ Boxhtml_div  ,'style="display: table-cell; width: 50%; float:left;"')
    txt2 = html_div( Conehtml_div+Rectanglehtml_div, 'style="display: table-cell; width: 50%; float:right;"')
    txt = html_div( txt1+txt2 , 'style="display: table; width: 100%"')
    return block(txt, 'Sky Search', id="skyareaFieldSet")


def Filter_block():
    txt = """
           <label for="optionFilter">
           <span title="Python syntax." class="tooltip"> Condition</span>:
           <input type="text" size="110" id="optionFilter"
           placeholder="(Jmag-Hmag &lt; 2.0) &amp; (Jmag &gt; 20) | (log10(Jflux) &gt; 1.2e-13)">
        </label>
    """
    return block( txt, 'Filter' )


def Output_block():
    txt = """
            <input type="radio" id="radioNoLimit" name="limitRadio">
        <label for="radioNoLimit"> No limit </label>
            <input type="radio" id="radioLimit" name="limitRadio" checked="checked">
        <label for="radioLimit"> Limit: </label>
        <input type="number" step="1" min="1" max="1000000000" value="100" id="outputLimitN">
            <br>
        """
    web = """
            <input type="radio" id="radioOutputWeb" name="outputRadio" checked="checked">
        <label for="radioOutputWeb"> Web page </label>
        """
    samp = """
            <input type="radio" id="radioOutputSAMP" name="outputRadio">
        <label for="radioOutputSAMP"> SAMP </label>
            <button id="buttonSAMP" type="button">
                <img src="content/samp_disconnected.png" id="imgDiscSAMP" title="Not connected. Click to register to a SAMP hub." width="15" height="15" border="0">
                <img src="content/samp_connected.png" id="imgConnSAMP" title="Connected to a SAMP hub. Click to disconnect." width="15" height="15" border="0" style="display: none; ">
            </button>
        """
    tsv = """
            <input type="radio" id="radioOutputTSV" name="outputRadio">
        <label for="radioOutputTSV"> TSV ('\\t') </label>"""
    csv = """
            <input type="radio" id="radioOutputCSV" name="outputRadio">
        <label for="radioOutputCSV"> CSV (',') </label> """
    fits = """
            <input type="radio" id="radioOutputFITS" name="outputRadio">
        <label for="radioOutputFITS"> FITS </label> """
    json = """
            <input type="radio" id="radioOutputJSON" name="outputRadio">
        <label for="radioOutputJSON"> JSON </label>"""

    votable = """
            <input type="radio" id="radioOutputVOT" name="outputRadio">
        <label for="radioOutputVOT"> VOTable </label> """

    plot = """
            <input type="radio" id="radioOutputPLOT" name="outputRadio">
        <label for="radioOutputPLOT"> Plot  </label>"""
    return block( txt + web + tsv + csv + fits + json + samp + plot, 'Output')


def Plot_block():
    form_div =  html_div( """
                <div id="PlotCaption">
                   <!--a href="#">Quick Plot</a></h3-->
                   <span><b>Quick Plot</b></span>
                                   <a href=""><img src="img/sort_desc.png" alt="rolllup" title="Show/hide plotting tools"></a>
                </div>
                <!-- <div id="plotToggleDiv" style="display: none;"> -->
                <div id="plotToggleDiv" style="display: block;">

                <p> Quick Visualization tools, mainly plot functions from matplotlib </p>

                <!-- Plotting functions -->

                    <label for="optionPlotFunction"> Plot type: </label>
                    <select id="plotFuncSelect">
                       <option value="plot" selected="selected">plot</option>
                       <option value="hist">hist</option>
                       <option value="scatter">scatter</option>
                       <option value="densityMap">density</option>
                    </select>

                <!-- Plotting options -->

                    <div>
                    <label for="Xaxis">
                    <span title="See EZtable Documentation" class="tooltip"> X-axis</span>:
                    <input type="text" size="30" id="xPlotVal" placeholder="A + B">
                    <input type="checkbox" name="xRevChk" value="xrev" />
                    Reverse
                    <input type="checkbox" name="xLogChk" value="xlog" />
                    Log
                    </label>
                    </div>
                    <div>
                    <label for="Yaxis">
                    <span title="See EZtable Documentation" class="tooltip"> Y-axis</span>:
                    <input type="text" size="30" id="yPlotVal" placeholder="log10(C)">
                    <input type="checkbox" name="yRevChk" value="yrev" />
                    Reverse
                    <input type="checkbox" name="yLogChk" value="ylog" />
                    Log
                    </label>
                    </div>
                    <div>
                    <label for="optionPlot">
                    <span title="See Matplotlib Documentation" class="tooltip"> Options</span>:
                    <input type="text" size="50" id="optionPlot" placeholder="lw=2, color='r', alpha=0.5">
                    </label>
                    </div>

                    <form id="plotform" >
                        <input type="submit" value="Submit" id="submit">
                     <input type="submit" value="Plot">
                    </form>
                </div>
                """
            , 'id="plotDiv", style="display: table-cell; width: 50%; float:left;"')
    txt = block(form_div, 'EzPlot', id="plotblock")
    return txt


def Submit_block():
    txt  = """ <input type="submit" value="Submit" id="submit">"""
    txt += """<img src="content/progressbar.gif" alt="" id="progressbar" style="display: none; ">"""
    txt += '<br>'
    txt += '<label id="dataUrl"></label>'
    return block(txt, '')


def Result_block():
    return block('', 'Query results', id="queryResultFieldSet")


def site_info():
    txt = html_list([ html_bf('UNDER DEVELOPMENT!!'),
        'This page is a prototype which provides multiple protocl access to a <b> python table server </b> (in dev.).' ,
        'This web page is very inspired from '+ html_link('http://cdsxmatch.u-strasbg.fr/QueryCat/catfs.html','CDSCatFileSearch')+ ' webpage from F.X. Pineau',
        'This page is entirely generated and served with Python, using '+ html_url('http://bottlepy.org/','Bottle.py') + 'and some javascripts.',
        'For more information, contact me at mfouesn "at" uw "dot" edu' ])
    return txt


def site_title():
    txt = html_h1(html_bf('EZTap: Python Easy Table Access Protocol (v%s)' % __version__))
    txt += html_br() + 'By %s <br><br>\n' % html_em(__author__)
    txt = '<img src="content/mydb.png" id="logo" title="mydb" width="220"  style="float:left;margin:10px;"/>'+html_div(txt )
    return txt


def site_footer():
    txt = html_image('https://lh4.googleusercontent.com/-nhBkb2smvJ0/Trhs4L9E_4I/AAAAAAAAABk/OyUahWQnt5A/s241/python-logo.png', 'python.org', 'height=30px ', link=False)
    txt += html_image('http://bottlepy.org/docs/dev/_static/logo_nav.png',
            'Bottle.org', 'height=30px style=margin-left:5px;', link=False)
    return txt


@route('/')
@page_template
def index():
    txt  = html_div(site_title(), 'style=margin-bottom:10px;')
    txt +=  block(site_info(), 'Information about this page')

    formdiv  = html_div(Catalog_block(),'style=margin-top:30px;' )
    formdiv += html_div(Sky_block() )
    formdiv += html_div(Filter_block() )
    formdiv += html_div(Output_block() )
    formdiv += html_div(Submit_block() )

    txt += form(formdiv, 'id=catfileform')
    txt += html_div(Result_block() )
    txt += html_div(Plot_block() )

    txt +=  html_div(site_footer(), 'style=margin-top:30px;')

    print request.query.keys()
    for k in request.query.keys():
        print '%s=%s' % (k,request.query[k])

    txt = html_div(txt, 'id="main" ')
    return txt
