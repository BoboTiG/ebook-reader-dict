#!/bin/bash

# This file is part of pnglatex <https://github.com/mneri/pnglatex>.
# Copyright Massimo Neri <hello@mneri.me> and all the contributors.

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

BACKGROUND=White
BORDER=
DPI=
ENVIRONMENT=\$
FOREGROUND=Black
FORMULA=
HEADER=
HELP=0
LOGFILE=
MARGIN=
META=1
OPTIMIZE=0
PACKAGES=
PADDING=
PNGFILE=
SHOWVERSION=0
SILENT=0
SIZE=11
TEXFILE=
declare -r VERSION=0.12

# Add margin, border and padding to the image.
function box {
    if [ "$PADDING" ]; then
        convert $PNGFILE -bordercolor $BACKGROUND -border $(scale $PADDING) $PNGFILE
    fi

    if [ "$BORDER" ]; then
        convert $PNGFILE -bordercolor $BORDER -border $(scale 1) $PNGFILE
    fi

    if [ "$MARGIN" ]; then
        convert $PNGFILE -bordercolor $BACKGROUND -border $(scale $MARGIN) $PNGFILE
    fi
}

# Remove temporary files.
function clean {
    rm -rf $TMPDIR
}

# Collapse multiple subsequent spaces in a string.
#
# @param $1 the string to collapse.
# @return echoes the collapsed string.
function collapse {
    echo $1 | sed -r -e 's/[[:space:]]+/ /'
}

# Get screen's dpi.
#
# @return the dpi resolution of the screen.
function dpi {
    local VALUE

    if exists xdpyinfo; then
        VALUE=$(xdpyinfo 2> /dev/null | grep resolution | sed -r 's/^[^0-9]+([0-9]+)x.*$/\1/')
    fi

    if [ ! "$VALUE" ]; then
        VALUE=96
    fi

    echo $VALUE
}

# Check if the specified command is installed on the system.
#
# @param $1 the command to test.
# @return true if the command is installed on the system, false otherwise.
function exists {
    local COMMAND=$1
    return $(command -v $COMMAND &> /dev/null)
}

# Generate the png image.
function generate {
    local BEGINENV
    local ENDENV
    local PREFIX
    local MESSAGE
    local TMPDIR
    local SUFFIX

    if [ ! "$FORMULA" ]; then
        MESSAGE="Interactive mode (<Ctrl-D> to end): "

        while read -p "$MESSAGE" -r LINE; do
            MESSAGE=
            FORMULA="$FORMULA $LINE"
        done
    fi

    FORMULA=$(trim "$FORMULA")
    FORMULA=$(collapse "$FORMULA")

    if [ ! "$FORMULA" ]; then
        echo "No input formula." >&2
        exit 1
    fi

    TMPDIR="$(mktemp -d)"
    TEXFILE="$(mktemp -p $TMPDIR fXXX.tex)"

    if [ "$ENVIRONMENT" = '$' ] || [ "$ENVIRONMENT" = '$$' ]; then
        BEGINENV=$ENVIRONMENT
        ENDENV=$ENVIRONMENT
    else
        BEGINENV="\begin{$ENVIRONMENT}"
        ENDENV="\end{$ENVIRONMENT}"
    fi

    PREFIX="\documentclass[${SIZE}pt]{article}$PACKAGES\pagestyle{empty}$HEADER\begin{document}$BEGINENV"
    SUFFIX="$ENDENV\end{document}"

    echo "$PREFIX $FORMULA $SUFFIX" > $TEXFILE

    if [ "$LOGFILE" ]; then
        cat $TEXFILE > $LOGFILE
    fi

    latex -halt-on-error -interaction=nonstopmode -output-directory=$TMPDIR $TEXFILE \
        | tee -a $LOGFILE \
        | sed -n '/^!/,/^ /p' >&2

    if [ ${PIPESTATUS[0]} -ne 0 ]; then
        clean
        exit 1
    fi

    if [ ! "$PNGFILE" ]; then
        PNGFILE="$(mktemp -p $PWD fXXX.png)"
    fi

    if [ ! "$DPI" ]; then
        DPI=$(dpi)
    fi

    dvipng -bg $BACKGROUND -D $DPI -fg $FOREGROUND -o $PNGFILE -q --strict -T tight ${TEXFILE%.tex}.dvi \
        | tee -a $LOGFILE \
        > /dev/null

    if [ "$PADDING" ] || [ "$BORDER" ] || [ "$MARGIN" ]; then
        box
    fi

    if [ $OPTIMIZE -eq 1 ]; then
        optimize
    fi

    if [ $META -eq 1 ]; then
        meta
    fi

    if [ $SILENT -eq 0 ]; then
        readlink -f $PNGFILE
    fi

    clean
}

# Entry point of the script.
function main {
    if ! exists latex || ! exists dvipng; then
        echo "pnglatex requires latex and dvipng packages." >&2
        exit 1
    fi

    parse "$@"

    if [ $HELP -eq 1 ]; then
        usage
        exit 0
    fi

    if [ $SHOWVERSION -eq 1 ]; then
        version
        exit 0
    fi

    if [ "$FORMULA" ] && [ "$REVERSE" ]; then
        echo "Incompatible options: use either -f or -r, not both." >&2
        exit 1
    fi

    if [ "$REVERSE" ]; then
        if ! exists identify; then
            echo "Getting formula from image requires imagemagick package." >&2
            exit 1
        fi
    fi

    if [ "$PADDING" ] || [ "$BORDER" ] || [ "$MARGIN" ]; then
        if ! exists convert; then
            echo "Paddings, borders and margins require imagemagick package." >&2
            exit 1
        fi
    fi

    if [ $OPTIMIZE -eq 1 ]; then
        if ! exists optipng; then
            echo "Optimization requires optipng package." >&2
            exit 1
        fi
    fi

    if [ "$REVERSE" ]; then
        reverse
    else
        generate
    fi
}

# Return true if the specified string matches the specified regular expression
#
# @param $1 The string to test.
# @param $2 The pattern to match.
# @return true if the string matches the pattern, false otherwise.
function match {
    local PATTERN=$2
    local TEXT=$1

    return $(echo $TEXT | egrep $PATTERN &> /dev/null);
}

# Add metadata to the image.
function meta {
    if exists convert; then
        convert -set latex:formula "${FORMULA//\\/\\\\}" -set generator "pnglatex $VERSION" $PNGFILE $PNGFILE
    fi
}

# Use optipng to optimize the image.
#
# @return echoes optipng output.
function optimize {
    if [ "$LOGFILE" ]; then
        optipng -f0-5 -zc1-9 -zm1-9 -zs0-3 $PNGFILE >> $LOGFILE
    else
        optipng -f0-5 -quiet -zc1-9 -zm1-9 -zs0-3 $PNGFILE
    fi
}

# Parse command line arguments.
function parse {
    while getopts b:B:d:e:f:F:hH:l:m:Mo:Op:P:r:s:Sv ARG; do
        case $ARG in
            b)
                BACKGROUND=$OPTARG
                ;;
            B)
                BORDER=$OPTARG
                ;;
            d)
                DPI=$OPTARG

                if ! match $DPI '^[1-9][0-9]*$'; then
                    echo "Invalid dpi." >&2
                    exit 1
                fi
                ;;
            e)
                ENVIRONMENT=$OPTARG
                ;;
            f)
                FORMULA=$OPTARG
                ;;
            F)
                FOREGROUND=$OPTARG
                ;;
            h)
                HELP=1
                ;;
            H)
                HEADER=\\input\{$OPTARG\}
                ;;
            l)
                LOGFILE=$OPTARG
                ;;
            m)
                MARGIN=$OPTARG

                if ! match $MARGIN '^[0-9]+(x[0-9]+)?$'; then
                    echo "Invalid margin." >&2
                    exit 1
                fi
                ;;
            M)
                META=0
                ;;
            o)
                PNGFILE=$OPTARG
                ;;
            O)
                OPTIMIZE=1
                ;;
            p)
                OIFS=$IFS
                IFS=":"
                PLIST=$OPTARG

                for P in $PLIST; do
                    PACKAGES=$PACKAGES\\usepackage{$P}
                done

                IFS=$OIFS
                ;;
            P)
                PADDING=$OPTARG

                if ! match $PADDING '^[0-9]+(x[0-9]+)?$'; then
                    echo "Invalid padding." >&2
                    exit 1
                fi
                ;;
            r)
                REVERSE=$OPTARG
                ;;
            s)
                SIZE=$(echo $OPTARG | sed 's/pt//')

                if ! match $SIZE '^[1-9][0-9]*$'; then
                    echo "Invalid font size." >&2
                    exit 1
                fi
                ;;
            S)
                SILENT=1
                ;;
            v)
                SHOWVERSION=1
                ;;
            ?)
                exit 1
        esac
    done
}

# Print the LaTeX formula starting from a png image.
#
# @return echoes the LaTeX formula.
function reverse {
    if [ ! -e "$REVERSE" ] || [ ! -r "$REVERSE" ]; then
        echo "Can't open file." >&2
        exit 1
    fi

    echo $(identify -verbose "$REVERSE" | grep 'latex:formula:' | sed -r 's/[ \t]*latex:formula:[ \t]*(.*)/\1/')
}

# Scales the specified dimensions to the wanted dpi.
#
# @param $1 the dimension string, in the form of 'mxn', where m and n are integers.
# @return echoes the scaled dimension string.
function scale {
    local BASEDPI=$(dpi)
    local WIDTH=$(($(echo $1 | sed -r 's/x.*//') * $DPI / $BASEDPI))
    local HEIGHT=$(($(echo $1 | sed -r 's/.*x//') * $DPI / $BASEDPI))

    echo ${WIDTH}x${HEIGHT}
}

# Remove spaces from the beginning and the end of a string.
#
# @param $1 the string to trim.
# @return echoes the string.
function trim {
    echo $1 | sed -r -e 's/^[[:space:]]+//' -e 's/[[:space:]]+$//'
}

# Print usage message.
#
# @return echoes the usage message.
function usage {
    echo "pnglatex $VERSION - Write LaTeX formulas into PNG files."
    echo "Copyright Massimo Neri <hello@mneri.me> and all the contributors."
    echo
    echo "List of options:"
    echo "  -b <color>       Set the background color."
    echo "  -B <color>       Set the border color."
    echo "  -d <dpi>         Set the output resolution to the specified dpi."
    echo "  -e <environment> Set the environment."
    echo "  -f <formula>     The LaTeX formula."
    echo "  -F <color>       Set the foreground color."
    echo "  -h               Print this help message."
    echo "  -H <file>        Insert the content of the specified file in the preamble."
    echo "  -l <file>        Log file."
    echo "  -m <margin>      Set the margin."
    echo "  -M               Strip meta information."
    echo "  -o <file>        Specify the output file name."
    echo "  -O               Optimize the image."
    echo "  -p <packages>    A colon separated list of LaTeX package names."
    echo "  -P <padding>     Set the padding."
    echo "  -r <file>        Read an image and print the LaTeX formula."
    echo "  -s <size>        Set the font size."
    echo "  -S               Silent mode: don't print image file name."
    echo "  -v               Show version."
    echo
    echo "Examples:"
    echo "  pnglatex -f \"E=mc^2\""
    echo "  pnglatex -e displaymath -f \"\sum_{i=0}^n i=\frac{n(n+1)}{2}\""
    echo "  pnglatex -b Transparent -p amssymb:amsmath -P 5x5 -s 12 -f \"A\triangleq B\""
}

# Print pnglatex version.
#
# @return echoes the version.
function version {
    echo $VERSION
}

trap "clean" SIGINT SIGTERM
main "$@"
