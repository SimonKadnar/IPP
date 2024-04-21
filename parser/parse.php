<?php 

//Autor: Šimon Kadnár xkadna00

ini_set('display_errors', 'stderr');

$global = 0;   //premenna rozhoduje o tom ci na konci xml vystupu bude </program> 

//generovanie xml po riadkoch
function xml($tmp)
{
    static $instr_num = 0;  //cislo instruckie
    $arg_num = 0;   //cislo argumentu u danej instrukcie
    $guard = 0;     
    $instruct = 0;

    $tmp2 = explode(" ",$tmp);

    for($i = 0; $i < substr_count($tmp, ' ')+1; $i++)   //bezi nazakledne poctu medzier na riadku
    {
        if(preg_match('/^ *$/',$tmp2[$i])) //filtracia medzier
        { 

        }
        else if(preg_match('/^ *#.*$/',$tmp2[$i]))  //ak nasleduje komentar tak nechceme dalej vypisovat instrukcie
        {
            echo " </instruction>\n";
            return;
        }

        //guard = 0 znaci ze este nebol pouzity ziadny prikaz na danom riadku a teda jedna sa o instrukciu
        else if( (preg_match('/^ *[a-zA-Z2]+ *$/',$tmp2[$i])) && ($guard == 0))  
        { 
            $GLOBALS['global'] = 1;   //vieme ze xml vystup bude obsahovat aspon jeden prikaz a tedda moze dojst k vypisu </program>
            $guard++;
            $instr_num++;
            echo " <instruction order=\"".$instr_num."\" opcode=\"";

            for($j = 0; strlen($tmp2[$i]) != $j ; $j++) 
            {
                if($tmp2[$i][$j] > '91' )
                    $tmp2[$i][$j] = strtoupper($tmp2[$i][$j]);
                if($tmp2[$i][$j] != "\n" )
                    echo $tmp2[$i][$j];
            }
            echo "\">\n";

            //v pripade ze sa jedna o instrukciu ktora nema ziadne parametre tak nechceme aby na konci vypisalo </instruction>
            if(preg_match('/^ *(([Cc][Rr][Ee][Aa][Tt][Ee][Ff][Rr][Aa][Mm][Ee])|([Pp][Uu][Ss][Hh][Ff][Rr][Aa][Mm][Ee])|([Pp][Oo][Pp][Ff][Rr][Aa][Mm][Ee])|([Rr][Ee][Tt][Uu][Rr][Nn])|([Bb][Rr][Ee][Aa][Kk])).*$/',$tmp2[$i]))
            {
                $instruct = 1;
            }
        }

        //////////////////////////////////////////////////////////////////////////////////

        else if(preg_match('/^ *(bool@false)( *| *#.*)$/',$tmp2[$i]))           //BOOLfalse
        { 
            $arg_num++;
            echo "  <arg".$arg_num." type=\"bool\">false</arg".$arg_num.">\n";
        }
        else if(preg_match('/^ *(bool@true)( *| *#.*)$/',$tmp2[$i]))            //BOOLtrue
        { 
            $arg_num++;
            echo "  <arg".$arg_num." type=\"bool\">true</arg".$arg_num.">\n";
        }
        else if(preg_match('/^ *(int@(\+|\-)?[\d]+) *$/',$tmp2[$i]))            //INT
        { 
            $arg_num++;
            echo "  <arg".$arg_num." type=\"int\">";

            for($j = 4; strlen($tmp2[$i]) != $j ; $j++) 
            {
                if($tmp2[$i][$j] == "#" )   //v pripade ze dana premenna obsahuje tesne za sebov komentar nechceme aby bol sucastou vypisu v xml 
                    break;
                if($tmp2[$i][$j] != "\n" )  
                    echo $tmp2[$i][$j];
            }
            echo "</arg".$arg_num.">\n";
        }
        else if(preg_match('/^ *(string@*.*) *$/',$tmp2[$i]))    //STRING 
        { 
            $arg_num++;
            echo "  <arg".$arg_num." type=\"string\">";

            for($j = 7; strlen($tmp2[$i]) != $j ; $j++) 
            {
                if($tmp2[$i][$j] == "#" )
                    break;
                if($tmp2[$i][$j] == "&" )
                    echo "&amp;";
                else if($tmp2[$i][$j] != "\n" )
                    echo $tmp2[$i][$j];
            }
            echo "</arg".$arg_num.">\n";
        }
        else if(preg_match('/^ *(([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*))) *$/',$tmp2[$i]))    //premenna
        { 
            $arg_num++;
            echo "  <arg".$arg_num." type=\"var\">";

            for($j = 0; strlen($tmp2[$i]) != $j ; $j++) 
            {
                if($tmp2[$i][$j] == "#" )
                    break;
                if($tmp2[$i][$j] != "\n" )
                    echo $tmp2[$i][$j];
            }
            echo "</arg".$arg_num.">\n";
        }
        else if(preg_match('/^ *(int|string|bool) *$/',$tmp2[$i]))    //type
        { 
            $arg_num++;
            echo "  <arg".$arg_num." type=\"type\">";

            for($j = 0; strlen($tmp2[$i]) != $j ; $j++) 
            {
                if($tmp2[$i][$j] == "#" )
                    break;
                if($tmp2[$i][$j] != "\n" )
                    echo $tmp2[$i][$j];
            }
            echo "</arg".$arg_num.">\n";
        }
        else if(preg_match('/^ *([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) *$/',$tmp2[$i]))    //label
        { 
            $arg_num++;
            echo "  <arg".$arg_num." type=\"label\">";

            for($j = 0; strlen($tmp2[$i]) != $j ; $j++) 
            {
                if($tmp2[$i][$j] == "#" )
                    break;
                if($tmp2[$i][$j] != "\n" )
                    echo $tmp2[$i][$j];
            }
            echo "</arg".$arg_num.">\n";
        }
    }
    if($instruct == 0)
        echo " </instruction>\n";
}

function right_lexi($tmp,$file)
{
        exit(23);
}

if($argc > 1 )          //--help
{
    if($argc > 2 )
    {
        exit(10);
    }

    if(preg_match('/^ *--help$/',$argv[1]))
    {
        echo "print help: php parse.php --help \n";
        echo "load file and print output on stdout: php IPP.php < file_name_in \n";
        echo "load file and print output in outfile: php IPP.php < file_name_in > file_name_out\n";
        return 0;
    }
    else
    {
        exit(10);
    }
}

$file = fopen('php://stdin',"r");
 
$guard = 0;
$i = -1;
$tmp2;

while($tmp =fgets($file))
{ 
    $i++;
    $tmp2[$i] = $tmp;

    if(($guard == 0) && ( 0 == preg_match('/^( *| *#.*)$/',$tmp))) //overenie zda vstupny subor obsahuje hlavicku .IPPcode22
    {
        if( 0 == preg_match('/^ *\.[Ii][Pp][Pp][Cc][Oo][Dd][Ee]22( *| *#.*)$/',$tmp))
        {
            fclose($file);
            exit(21);
        }
        else
        {
            $guard++;
        }
    }

    /////////////////////////////////////////////////////////////////////////////NIC

    else if(preg_match('/^ *[Cc][Rr][Ee][Aa][Tt][Ee][Ff][Rr][Aa][Mm][Ee].*$/',$tmp))    //vstup do vetvy zacinajuca funkciou "createframe"
    {
        if( 0 == preg_match('/^ *[Cc][Rr][Ee][Aa][Tt][Ee][Ff][Rr][Aa][Mm][Ee]( *| *#.*)$/',$tmp))    //overenie zda neobshauje nejaku chybu
        {
            right_lexi($tmp,$file); // v pripade chyby sa rozhodne ci sa jedna o chybu 22 alebo 23
        }
    }
    else if(preg_match('/^ *[Pp][Uu][Ss][Hh][Ff][Rr][Aa][Mm][Ee].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Pp][Uu][Ss][Hh][Ff][Rr][Aa][Mm][Ee]( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Pp][Oo][Pp][Ff][Rr][Aa][Mm][Ee].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Pp][Oo][Pp][Ff][Rr][Aa][Mm][Ee]( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Rr][Ee][Tt][Uu][Rr][Nn].*$/',$tmp ))
    {
        if( 0 == preg_match('/^ *[Rr][Ee][Tt][Uu][Rr][Nn]( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Bb][Rr][Ee][Aa][Kk].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Bb][Rr][Ee][Aa][Kk]( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    /////////////////////////////////////////////////////////////////////////////////////LABEL VSETKO VSETKO

    else if(preg_match('/^ *[Jj][Uu][Mm][Pp][Ii][Ff][Ee][Qq].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Jj][Uu][Mm][Pp][Ii][Ff][Ee][Qq] +([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        } 
    }
    else if(preg_match('/^ *[Jj][Uu][Mm][Pp][Ii][Ff][Nn][Ee][Qq].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Jj][Uu][Mm][Pp][Ii][Ff][Nn][Ee][Qq] +([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }  
    }

    /////////////////////////////////////////////////////////////////////////LABEL

    else if(preg_match('/^ *[Cc][Aa][Ll][Ll].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Cc][Aa][Ll][Ll] +([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ll][Aa][Bb][Ee][Ll].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ll][Aa][Bb][Ee][Ll] +([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Jj][Uu][Mm][Pp].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Jj][Uu][Mm][Pp] +([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    ///////////////////////////////////////////////////////////////////////VSETKO

    else if(preg_match('/^ *[Pp][Uu][Ss][Hh][Ss] .*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Pp][Uu][Ss][Hh][Ss] +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ww][Rr][Ii][Tt][Ee].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ww][Rr][Ii][Tt][Ee] +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ee][Xx][Ii][Tt].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ee][Xx][Ii][Tt] +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Dd][Pp][Rr][Ii][Nn][Tt].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Dd][Pp][Rr][Ii][Nn][Tt] +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    ////////////////////////////////////////////////////////////////////////////////PREMENNA

    else if(preg_match('/^ *[Pp][Oo][Pp][Ss].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Pp][Oo][Pp][Ss] +(([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Dd][Ee][Ff][Vv][Aa][Rr].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Dd][Ee][Ff][Vv][Aa][Rr] +(([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    ////////////////////////////////////////////////////////////////////////////////PREMENNA VSETKO
    
    else if(preg_match('/^ *[Mm][Oo][Vv][Ee].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Mm][Oo][Vv][Ee] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ii][Nn][Tt]2[Cc][Hh][Aa][Rr].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ii][Nn][Tt][2][Cc][Hh][Aa][Rr] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ss][Tt][Rr][Ll][Ee][Nn].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ss][Tt][Rr][Ll][Ee][Nn] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Tt][Yy][Pp][Ee].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Tt][Yy][Pp][Ee] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*))+ +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    /////////////////////////////////////////////////////////////////Premenna Typ

    else if(preg_match('/^ *[Rr][Ee][Aa][Dd].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Rr][Ee][Aa][Dd] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +(int|string|bool)( *| *#.*)$/',$tmp))
        {
                right_lexi($tmp,$file);
        }
    }

    ///////////////////////////////////////////////////////////////////////PREMENNA VSETKO VSETKO

    else if(preg_match('/^ *[Aa][Dd][Dd].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Aa][Dd][Dd] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ss][Uu][Bb].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ss][Uu][Bb] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Mm][Uu][Ll].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Mm][Uu][Ll] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ii][Dd][Ii][Vv].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ii][Dd][Ii][Vv] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    else if(preg_match('/^ *[Ll][Tt].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ll][Tt] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Gg][Tt].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Gg][Tt] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ee][Qq].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ee][Qq] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    else if(preg_match('/^ *[Aa][Nn][Dd].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Aa][Nn][Dd] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Oo][Rr].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Oo][Rr] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Nn][Oo][Tt].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Nn][Oo][Tt] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }

    else if(preg_match('/^ *[Ss][Tt][Rr][Ii]2[Ii][Nn][Tt].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ss][Tt][Rr][Ii]2[Ii][Nn][Tt] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Cc][Oo][Nn][Cc][Aa][Tt].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Cc][Oo][Nn][Cc][Aa][Tt] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Gg][Ee][Tt][Cc][Hh][Aa][Rr].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Gg][Ee][Tt][Cc][Hh][Aa][Rr] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        }
    }
    else if(preg_match('/^ *[Ss][Ee][Tt][Cc][Hh][Aa][Rr].*$/',$tmp))
    {
        if( 0 == preg_match('/^ *[Ss][Ee][Tt][Cc][Hh][Aa][Rr] +([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true))) +((([G]|[L]|[T])[F]@([_\-\$&%\*!\?a-zA-Z]{1}([_\-\$&%\*!\?a-zA-Z0-9]*)))|(int@(\+|\-)?[\d]+)|(string@(([^\\\])|(\\\[\d]{3}))*)|(nil@nil)|(bool@(false|true)))( *| *#.*)$/',$tmp))
        {
            right_lexi($tmp,$file);
        } 
    }

    ////////////////////////////////////////////////////////////////////////////////////komentar

    else if(preg_match('/^ *#.*$/',$tmp))
    {

    }

    ////////////////////////////////////////////////////////////////////////////////////novy riadok

    else if(preg_match('/^ *(\n*)$/',$tmp))
    {

    }

    ////////////////////////////////////////////////////////////////////////////////////nezname veci
    
    else
    {
        exit(22);
    }
}

////////////////////////////////////////////////////////////////XML

echo "<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n";
echo "<program language=\"IPPcode22\">\n";

for($j = 0; $j != $i+1;$j++)
{
    if((0 == preg_match('/^ *$/',$tmp2[$j])) && (0 == preg_match('/^ *#.*$/',$tmp2[$j])) && (0 == preg_match('/^ *\.[Ii][Pp][Pp][Cc][Oo][Dd][Ee]22( *| *#.*)$/',$tmp2[$j])) )
    xml($tmp2[$j]);
}

if ($GLOBALS['global'] == 1)
    echo "</program>\n";

if (!fclose($file)) 
{
    echo "Cannot close: file";
    var_dump($file);
}

?>