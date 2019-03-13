# ----------------------------------------------------------------------
# Template


class TemplateMixin(object):
    # TODO Template  part
    """
    Define a HTML template for reports customerization and generation.

    Overall structure of an HTML reports

    HTML
    +------------------------+
    |<html>                  |
    |  <head>                |
    |                        |
    |   STYLESHEET           |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </head>               |
    |                        |
    |  <body>                |
    |                        |
    |   HEADING              |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   REPORT               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |   ENDING               |
    |   +----------------+   |
    |   |                |   |
    |   +----------------+   |
    |                        |
    |  </body>               |
    |</html>                 |
    +------------------------+
    """

    STATUS = {
        0: 'pass',
        1: 'fail',
        2: 'error',
    }

    DEFAULT_TITLE = 'Unit Test Report'
    DEFAULT_DESCRIPTION = 'Selenium Test Report:'

    # ------------------------------------------------------------------------
    # HTML Template

    HTML_TMPL = r"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset='utf-8'/>
        <meta name='description' content=''/>
        <meta name='robots' content='noodp, noydir'/>
        <meta name='viewport' content='width=device-width, initial-scale=1'/>
        <meta id="timeStampFormat" name="timeStampFormat" content='MMM d, yyyy hh:mm:ss a'/>

        <link href='https://fonts.googleapis.com/css?family=Source+Sans+Pro:400,600' rel='stylesheet' type='text/css'>
        <link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">

        <link href='http://extentreports.com/resx/dist/css/extent.css' type='text/css' rel='stylesheet'/>

        <title>{title} - TestReport</title>
        {stylesheet}

    </head>

    <body class='extent standard default hide-overflow dark'>
    <div id='theme-selector' alt='切换主题，默认黑色' title='切换主题'>
        <span><i class='material-icons'>desktop_windows</i></span>
    </div>
    {heading}

    <div class='container'>
        {reports}
        {dashboard_view}
    </div>

    </body>
    {script_js}
    </html>
    """
    # variables: (title, generator, stylesheet, heading, heading, ending)

    # ------------------------------------------------------------------------
    # Stylesheet
    #
    # alternatively use a <link> for external style sheet, e.g.
    #   <link rel="stylesheet" href="$url" type="text/css">

    NAV = """
    <nav>
    <div class="nav-wrapper">
        <a href="#!" class="brand-logo blue darken-3">Extent</a>

        <!-- slide out menu -->
        <ul id='slide-out' class='side-nav fixed hide-on-med-and-down'>
            <li class='waves-effect active'>
               <a href='#!' view='test-view' onclick="configureView(0);chartsView('test');">
                  <i class='material-icons'>dashboard</i>
               </a>
            </li>
            <!-- <li class='waves-effect'><a href='#!' view='category-view' onclick="configureView(1)"><i
                    class='material-icons'>label_outline</i></a></li>
            <li class='waves-effect'><a href='#!' onclick="configureView(-1);chartsView('dashboard');"
                                        view='dashboard-view'><i class='material-icons'>track_changes</i></a></li> -->
        </ul>

        <!-- reports name -->
        <span class='reports-name'>Test Report: {title}</span>

        <!-- reports headline -->
        <span class='reports-headline'></span>

        <!-- nav-right -->
        <ul id='nav-mobile' class='right hide-on-med-and-down nav-right'>
            <li>
                <a href='#!'>
                    <span class='label suite-start-time blue darken-3'>Start_time: {start_time}</span>
                </a>
            </li>
            <li>
                <a href='#!'>
                    <span class='label blue darken-3'>Duration: {duration} </span>
                </a>
            </li>
            <li>
                <a href='#!'>
                    <span class='label blue darken-3'>result: {status} </span>
                </a>
            </li>
        </ul>
    </div>
</nav>
    """

    TEST_VIEW = """
    <div id='test-view' class='view'>

        %(control_section)s

        %(view_charts)s
        %(test_list)s

        <div class='subview-right left'>
            <div class='view-summary'>
                <h5 class='test-name'></h5>

                <div id='step-filters' class="right">
                    <span class="blue-text" status="info" alt="info" title="info"><i
                            class="material-icons">info_outline</i></span>
                    <span class="green-text" status="pass" alt="pass" title="pass">
                      <i class="material-icons">check_circle</i>
                    </span>
                    <span class="red-text" status="fail" alt="fail" title="fail"><i
                            class="material-icons">cancel</i></span>
                    <span class="red-text text-darken-4" status="fatal" alt="fatal" title="fatal"><i
                            class="material-icons">cancel</i></span>
                    <span class="pink-text text-lighten-1" status="error" alt="error" title="error"><i
                            class="material-icons">error</i></span>
                    <span class="orange-text" alt="warning" status="warning" title="warning"><i
                            class="material-icons">warning</i></span>
                    <span class="teal-text" status="skip" alt="skip" title="skip"><i
                            class="material-icons">redo</i></span>
                    <span status="clear" alt="Clear filters" title="Clear filters"><i
                            class="material-icons">clear</i></span>
                </div>
            </div>
        </div>
    </div>
    %(category_view)s

"""
    CONTROL_SECTION = """
    <section id='controls'>
            <div class='controls grey lighten-4'>
                <!-- test toggle -->
                <div class='chip transparent'>
                    <a class='dropdown-button tests-toggle' data-activates='tests-toggle' data-constrainwidth='true'
                       data-beloworigin='true' data-hover='true' href='#'>
                        <i class='material-icons'>warning</i> Status
                    </a>
                    <ul id='tests-toggle' class='dropdown-content'>
                        <li status='pass'><a href='#!'>Pass <i class='material-icons green-text'>check_circle</i></a>
                        </li>
                        <li status='fail'><a href='#!'>Fail <i class='material-icons red-text'>cancel</i></a></li>
                        <li status="skip"><a href="#!">Skip <i class="material-icons cyan-text">redo</i></a></li>
                        <li class='divider'></li>
                        <li status='clear' clear='true'><a href='#!'>Clear Filters <i
                                class='material-icons'>clear</i></a></li>
                    </ul>
                </div>
                <!-- test toggle -->

                <!-- category toggle -->
                <div class='chip transparent'>
                    <a class='dropdown-button category-toggle' data-activates='category-toggle'
                       data-constrainwidth='false' data-beloworigin='true' data-hover='true' href='#'>
                        <i class='material-icons'>local_offer</i> Category
                    </a>
                    <ul id='category-toggle' class='dropdown-content'>
                        %(suite_name)s
                        <li class='divider'></li>
                        <li class='clear'><a href='#!' clear='true'>Clear Filters</a></li>
                    </ul>
                </div>
                <!-- category toggle -->

                <!-- clear filters -->
                <div class='chip transparent hide'>
                    <a class='' id='clear-filters' alt='Clear Filters' title='Clear Filters'>
                        <i class='material-icons'>close</i> Clear
                    </a>
                </div>
                <!-- clear filters -->

                <!-- enable dashboard -->
                <div id='toggle-test-view-charts' class='chip transparent'>
                    <a class='pink-text' id='enable-dashboard' alt='Enable Dashboard' title='Enable Dashboard'>
                        <i class='material-icons'>track_changes</i> Dashboard
                    </a>
                </div>
                <!-- enable dashboard -->

                <!-- search -->
                <div class='chip transparent' alt='Search Tests' title='Search Tests'>
                    <a href="#" class='search-div'>
                        <i class='material-icons'>search</i> Search
                    </a>

                    <div class='input-field left hide'>
                        <input style="color: red" id='search-tests' type='text' class='validate browser-default'
                               placeholder='Search Tests...'>
                    </div>

                </div>
                <!-- search -->
            </div>
        </section>
    """
    # Category下的list
    SECTION_SUIT_NAME = """
    <li><a href='#'>%(name)s</a></li>
    """

    VIEW_CHARTS = """
    <div id='test-view-charts' class='subview-full'>

            <div id='test-view-charts' class='subview-full'>
                <div id='charts-row' class='row nm-v nm-h'>
                    <div class='col s12 m6 l6 np-h'>
                        <div class='card-panel nm-v'>
                            <div class='left panel-name'>Tests</div>
                            <div class='chart-box'>
                                <canvas id='parent-analysis' width='100' height='80'></canvas>
                            </div>
                            <div class='block text-small'>
                            <span class='tooltipped' data-position='top'><span
                                    class='strong'>%(pass_count)s</span> test(s) passed</span>
                                <span class='tooltipped' data-position='top'><span
                                        class='strong'>%(fail_count)s</span> test(s) failed</span>
                            </div>
                            <div class='block text-small'>
                            <span class='strong tooltipped' data-position='top'
                            >%(error_count)s</span>
                                test(s) errored
                            </div>
                        </div>
                    </div>

                    <div class='col s12 m6 l6 np-h'>
                        <div class='card-panel nm-v'>
                            <div class='left panel-name'>Suites</div>
                            <div class='chart-box'>
                                <canvas id='child-analysis' width='100' height='80'></canvas>
                            </div>
                            <div class='block text-small'>
                            <span id="pass_suites" class='tooltipped' data-position='top'>
                            </span>
                            </div>
                            <div class='block text-small'>
                                <span id="fail_suites" class='strong tooltipped' data-position='top'></span> suite(s)
                                failed
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    """

    SUBVIEW_LEFT = """
    <div class='subview-left left'>

            <div class='view-summary'>
                <h5>Suites</h5>
                <ul id='test-collection' class='test-collection'>
                %(test_collection)s
                </ul>
            </div>
    </div>
    """

    TEST_COLLECTION = """

    <li class="test displayed active has-leaf {status}" status="{status}" bdd="true" test-id="{test_collection_li_id}">
    <div class='test-heading'>
        <span class='test-name'>{desc}</span>
        <span class='test-time'>desc: {doc} </span>
        <span class="test-status right {status}">{status}</span>
    </div>
    <div class='test-content hide'>
        <div class='test-desc'>Pass: {Pass} ;
                                Fail: {fail} ;
                                Error: {error} ;
        </div>
        <div class='test-attributes'>
            <div class='category-list'>
                <span class='category label white-text'>{desc}</span>
            </div>
        </div>
        <ul class='collapsible node-list' data-collapsible='accordion'>
            {test_collection_ul_list}
        </ul>
    </div>
    """
    TEST_COLLECTION_UL_LIST = """

            <li class="node level-1 leaf {status}" status="{status}" test-id="{node_level}">
            <div class='collapsible-header'>
                <div class='node-name'>{desc}</div>
                <span class='node-time'>desc: {doc}</span>
                <span class="test-status right {status}">{status}</span>
            </div>
            <div class='collapsible-body'>
                <div class='category-list right'>
                    <span class='category label white-text'>{desc}</span>
                </div>
                <div class='node-steps'>
                    <table class='bordered table-results'>
                        <thead>
                        <tr>
                            <th>Status</th>
                            <th>Identity</th>
                            <th>Details</th>
                        </tr>
                        </thead>
                        <tbody>
                        {t_body}
                        </tbody>
                    </table>
                 </div>
             </div>
            </li>
    """
    TBODY = """
        <tr class='info' status='info'>
            <td class='status info' title='info' alt='info'><i
                    class='material-icons'>low_priority</i></td>
            <td class='timestamp'>stdout</td>
            <td class='step-details'>%(script)s</td>
        </tr>
        <tr class='info' status='info'>
            <td class='status info' title='info' alt='info'><i
                    class='material-icons'>low_priority</i></td>
            <td class='timestamp'>screenshot</td>
            <td class='step-details'>%(images)s
            </td>
        </tr>
    """
    CATEGORY_VIEW = """
    <div id='category-view' class='view hide'>
        <section id='controls'>
            <div class='controls grey lighten-4'>
                <!-- search -->
                <div class='chip transparent' alt='Search Tests' title='Search Tests'>
                    <a href="#" class='search-div'>
                        <i class='material-icons'>search</i> Search
                    </a>

                    <div class='input-field left hide'>
                        <input tyle="color: red;" id='search-tests' type='text'
                               class='validate browser-default'
                               placeholder='Search Tests...'>
                    </div>

                </div>
                <!-- search -->
            </div>
        </section>

        <div class='subview-left left'>

            <div class='view-summary'>
                <h5>Categories</h5>
                <ul id='category-collection' class='category-collection'>

                    <li class='category displayed active'>
                        <div class='category-heading'>
                            <span class='category-name'>All Suites</span>
                            <span class='category-status right'>
                                <span class='label pass'>%(Pass)s </span>
                                <span class='label fail'>%(fail)s</span>
                            </span>
                        </div>
                        <div class='category-content hide'>
                            <div class='category-status-counts'>
                                <span class='label green accent-4 white-text'>Passed: %(Pass)s</span>
                                <span class='label red lighten-1 white-text'>Failed: %(fail)s</span>
                                <span class='label blue lighten-1 white-text'>Errored: %(error)s</span>
                                <span class="label yellow darken-2 white-text">Skipped: </span>
                            </div>

                            <div class='category-tests'>
                                <table class='bordered table-results'>
                                    <thead>
                                    <tr>
                                        <th>Timestamp</th>
                                        <th>TestName</th>
                                        <th>Status</th>
                                    </tr>
                                    </thead>
                                    <tbody>
                                    %(category_tbody)s
                                    </tbody>
                                </table>
                            </div>
                        </div>
                    </li>
                    %(category_active)s
                <div class='subview-right left'>
            <div class='view-summary'>
                <h5 class='category-name'></h5>
            </div>
        </div>
    </div>


    """
    CATEGORY_TBODY = """
    <tr style="border: 1px solid #49cc90; background-color: rgba(73, 204, 144, .1)">
        <td>{start_time}</td>
        <td class='linked' test-id='{name}_{cid}'>{desc}</td>
        <td><span class="test-status {status}">{status}</span></td>
    </tr>
    <tr>
        <td></td>
        <td class='linked' test-id='暂未处理'>'暂未处理'</td>
        <td><span class="test-status {status}">{status}</span></td>
    </tr>

    """

    CATEGORY_ACTIVE = """
    <li class='category displayed active'>
        <div class='category-heading'>
            <span class='category-name'>%(desc)s</span>
            <span class='category-status right'>
                <span class='label pass'>%(Pass)s </span>
                <span class='label fail'>%(fail)s</span>
            </span>
        </div>
        <div class='category-content hide'>
            <div class='category-status-counts'>
                <span class='label green accent-4 white-text'>Passed: %(Pass)s</span>
                <span class='label red lighten-1 white-text'>Failed: %(fail)s</span>
                <span class='label blue lighten-1 white-text'>Errored: %(error)s</span>
            </div>

            <div class='category-tests'>
                <table class='bordered table-results'>
                    <thead>
                    <tr>
                        <th>Timestamp</th>
                        <th>TestName</th>
                        <th>Status</th>
                    </tr>
                    </thead>
                    <tbody>

                    </tbody>
                </table>
            </div>
        </div>
    </li>
    """
    DASHBOARD_VIEW = """
    <div id='dashboard-view' class='view hide'>
        <div class='card-panel transparent np-v'>
            <h5>Dashboard</h5>

            <div class='row'>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Pass
                        <div class='panel-lead'>{Pass}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Fail
                        <div class='panel-lead'>{fail}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Error
                        <div class='panel-lead'>{error}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Skip
                        <div class='panel-lead'></div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Start
                        <div class='panel-lead'>{start_time}</div>
                    </div>
                </div>
                <div class='col s2'>
                    <div class='card-panel r'>
                        Time Taken
                        <div class='panel-lead'>{duration} seconds</div>
                    </div>
                </div>
                <div class='col s4'>
                    <div class='card-panel'>
                        <span class='right label cyan white-text'>Categories</span>
                        <p>&nbsp;</p>
                        <table>
                            <tr>
                                <th>Name</th>
                                <th>Passed</th>
                                <th>Failed</th>
                                <th>Errored</th>
                                <th>Skipped</th>
                            </tr>
                            <tr>
                                <td>All Suites</td>
                                <td class="pass">{Pass}</td>
                                <td class="fail">{fail}</td>
                                <td class="error">{error}</td>
                                <td class="skip"></td>
                            </tr>

                                <tr>
                                    <td id="unknown"></td>
                                    <td class="pass"></td>
                                    <td class="fail"></td>
                                    <td class="error"></td>
                                    <td class="skip"></td>
                                </tr>
                        </table>
                    </div>
                </div>
            </div>
        </div>
    </div>
    """

    SCRIPT_JS = """
    <script>
        var test_suite_success = %(Pass)s;


        var statusGroup = {
            passParent: %(Pass)s,
            failParent: %(fail)s,
            fatalParent: 0,
            errorParent: %(error)s,
            warningParent: 0,
            skipParent: 0,
            exceptionsParent: 0,

            passChild: test_suite_success,
            failChild: %(fail)s,
            fatalChild: 0,
            errorChild: %(error)s,
            warningChild: 0,
            skipChild: 0,
            infoChild: 0,
            exceptionsChild: 0,

            passGrandChild: 0,
            failGrandChild: 0,
            fatalGrandChild: 0,
            errorGrandChild: 0,
            warningGrandChild: 0,
            skipGrandChild: 0,
            infoGrandChild: 0,
            exceptionsGrandChild: 0,
        };

    </script>

    <script src='http://extentreports.com/resx/dist/js/extent.js' type='text/javascript'></script>


    <script type='text/javascript'>
        $(window).off("keydown");
    </script>
    """
    STYLESHEET_TMPL = """
    <style type="text/css">
        .node.level-1 ul {
            display: none;
        }

        .node.level-1.active ul {
            display: block;
        }

        .card-panel.environment th:first-child {
            width: 30%;
        }
        .small_img{
            height: 180px;
            width: 100px;
            padding: 10px;
            float: left;
            background-repeat: no-repeat;
            background-position: center center;
            background-size: cover;
          }
        .black_overlay{
            display: none;
            position: absolute;
            top: 0%;
            left: 0%;
            width: 100%;
            height: 100%;
            background-color: white;
            z-index:1001;
            -moz-opacity: 0.8;
            opacity:.80;
            filter: alpha(opacity=80);
        }
        .big_img {
            cursor: pointer;
            display: none;
            position: absolute;
            height: 650px;
            left:50%;
            top: 50%;
            margin: -300px 0px 0px -200px;
            z-index:1002;
            overflow: auto;
        }
    </style>
"""

    # ------------------------------------------------------------------------
    # Heading
    #

    HEADING_ATTRIBUTE_TMPL = """去掉
    <p class='attribute'><strong>{name}:</strong> {value}</p>"""
    # variables: (name, value)

    # ------------------------------------------------------------------------
    # Report
    #

    REPORT_TMPL = """
    <p id='show_detail_line'>Show
    <a href='javascript:showCase(0)'>Summary</a>
    <a href='javascript:showCase(1)'>Failed</a>
    <a href='javascript:showCase(2)'>All</a>
    </p>
    <table id='result_table'>
    <colgroup>
    <col align='left' />
    <col align='right' />
    <col align='right' />
    <col align='right' />
    <col align='right' />
    <col align='right' />
    </colgroup>
    <tr id='header_row'>
        <td>Test Group/Test case</td>
        <td>Count</td>
        <td>Pass</td>
        <td>Fail</td>
        <td>Error</td>
        <td>View</td>
        <td>Screenshot</td>
    </tr>
    %(test_list)s
    <tr id='total_row'>
        <td>Total</td>
        <td>%(count)s</td>
        <td>%(Pass)s</td>
        <td>%(fail)s</td>
        <td>%(error)s</td>
        <td>&nbsp;</td>
        <td>&nbsp;</td>

    </tr>
    </table>
"""
    # variables: (test_list, count, Pass, fail, error)
    REPORT_IMAGE = r"""
    <img class="small_img" src="%(screenshot)s" onclick="document.getElementById('light_%(screenshot_id)s').style.display ='block';document.getElementById('fade_%(screenshot_id)s').style.display='block'"/>
    """

    REPORT_TEST_NO_OUTPUT_TMPL = r"""
<tr id='%(tid)s' class='%(Class)s'>
    <td class='%(style)s'><div class='testcase'>%(desc)s</div></td>
    <td colspan='5' align='center'>%(status)s</td>
</tr>
"""
    # variables: (tid, Class, style, desc, status)

    REPORT_TEST_OUTPUT_TMPL = r"""
    %(id)s: %(output)s
    """
    # variables: (id, output)
    REPORT_TEST_OUTPUT_IMAGE = r"""
    %(screenshot)s
    """
    REPORT_TEST_OUTPUT_CASEID = r"""
    %(case_id)s
    """
    # ------------------------------------------------------------------------
    # ENDING
    #

    ENDING_TMPL = """<div id='ending'>&nbsp;</div>"""
# -------------------- The end of the Template class -------------------
