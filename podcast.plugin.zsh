function podcast {
    local opt=$1
    case "$opt" in
    search)
        if [[ $2 == '' ]]; then
            echo "podcast search: please enter a search term"
            return 1
        fi

        _podcast_invoke_python $@
        ;;
    imfeelinglucky)
        _podcast_invoke_python 'random'
        ;;
    download)
        if [[ $2 == '' ]]; then
            echo "podcast download: please enter the short url of a dev.to podcast"
            return 1
        fi

        _podcast_download $2
        ;;
    info)
        if [[ $2 == '' ]]; then
            echo "podcast info: please enter the short url of a dev.to podcast"
            return 1
        fi

        _podcast_invoke_python $@
        ;;
    list)
        if [[ $2 == '' ]]; then
            echo "podcast list: please enter the page number"
            return 1
        fi

        if [[ $3 == '' ]]; then
            # by default, use 10 podcasts per page
            _podcast_invoke_python 'list' $2 10
        else
            _podcast_invoke_python 'list' $2 $3
        fi

        ;;
    "" | -h | --help)
        echo "Usage: podcast <option>"
        echo "-h, --help\n\tShow help information"
        echo "search <search_term>\n\tSearch recent podcasts for the search term"
        echo "imfeelinglucky\n\tShow a random podcast episode"
        echo "podcast download <short_url> <?download_dir>\n\tDownload a podcast"
        echo "\tIf the download directory is missing, this will download to ./podcasts"
        echo "info <short_url>\n\tDisplay the show art and any metadata"
        echo "list <pg_num> <pg_size>\n\tBrowse the list of podcasts page by page"
        ;;
    *)
        echo "Unknown option: $opt"
        return 1
        ;;
    esac
}

function _podcast_download {
    local pyscript="${0:A:h}/download.py"
    python3 $pyscript $@
}

function _podcast_invoke_python {
    local pyscript="${0:A:h}/podcast.py"
    python3 $pyscript $@
}

function _ascii_art() {
    if [[ $# < 1 ]]; then
        echo "1 argument that points to the img file path has to be specified"
        exit

    else

    fi

    filename="${1##*/}"
    dirname="${1%/*}"
    file=${1:t:r}

    if [[ "$filename" = "$dirname" ]]; then
        $dirname="."
    fi

    if [[ $(file -b $1) =~ JPEG ]]; then
        thumbnail=$1
    else
        thumbnail="$dirname/$file.jpg"
        sips -s format jpeg $1 --out "$dirname/$file.jpg" >/dev/null
    fi

    jp2a --width=80 --colors $thumbnail
}
