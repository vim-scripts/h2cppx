if(exists('b:h2cppx')) | finish | endif

let b:h2cppx = 1

if(exists('g:h2cppx'))  
    finish 
endif

let g:h2cppx = 1

"config variable
if(exists('g:h2cppx_python_path'))
    let s:python_path = g:h2cppx_python_path
else
    let s:python_path = 'python'
endif
if(exists('g:h2cppx_postfix'))
    let s:postfix = substitute(g:h2cppx_postfix,'\.',"","")
else
    let s:postfix = 'cpp'
endif
if(exists('g:h2cppx_template'))
    let s:template_file = g:h2cppx_template
else
    let s:template_file = 'template1'
endif


if(system(s:python_path . ' -c "import sys; print sys.version_info[0]"') != "2\n")
    echohl WarningMsg | echomsg "load h2cppx faild,python2.x is must need for h2cppx." | echohl None
    finish
endif

let s:installed_directory = expand('<sfile>:p:h:h')
let s:h2cppx_dir = s:installed_directory . "/h2cppx"
let s:h2cppx_path= s:h2cppx_dir . "/h2cppx.py"

if (stridx(s:template_file,'/') != 0)
    let s:template_file= s:installed_directory . "/h2cppx/template/" . s:template_file
endif
let s:config_file = findfile(".h2cppx_conf", ".;")
if (s:config_file != "")
    let s:config_file = fnamemodify(s:config_file,":p")
    let s:config_dir  = fnamemodify(s:config_file, ":p:h")
    let s:search_list = readfile(s:config_file)
    let s:i = 0
    while s:i < len(s:search_list)
        if (stridx(s:search_list[s:i],'/') != 0)
            let s:search_list[s:i] = s:config_dir . '/' . s:search_list[s:i]
        endif
        let s:i = s:i + 1
    endwhile
else
    let s:search_list = []
endif

"get full path
function s:fullpath(path)
    let dir = a:path
    let dir = fnamemodify(dir, ":p")
    if strlen(dir)!=0 && (stridx(dir,'/')!=0)
        let dir = fnamemodify(".",":p") . dir
    endif
    if strridx(dir,'/') != (strlen(dir)-1)
        let dir = dir . '/'
    endif
    return dir
endfunction

"full generate cpp file
function s:h2cppx(header_file, isClipboard)
    let filename = expand('%:r') . "." . s:postfix
    let cpp_file = findfile(filename, join(s:search_list,","))

    let cmd = printf('%s "%s" -t "%s" "%s" ', s:python_path, s:h2cppx_path, s:template_file, a:header_file)
    if ! (a:isClipboard == 1)
        if cpp_file == ""
            let dir = input("Cpp File not find, please enter the new file output directory: ")
            let cpp_file = s:fullpath(dir) . filename
        endif
        let cmd = cmd . " -o " . cpp_file
    endif
    let content = system(cmd)

    while 1
        if v:shell_error == 0
            if a:isClipboard == 1
                call setreg('"+', content )
                echo "Define code already copy to your clipboard,use p to paster!"
            else
                echo "Generate file " . cpp_file . " successful!"
            endif
        elseif v:shell_error == 1
            echo content
        elseif v:shell_error == 2
            echo content 
        elseif v:shell_error == 3
            echo content 
        elseif v:shell_error == 4
            let ans = input("file already exisit, force overwrite it?(yes/no): ")
            if toupper(ans) == "YES" || toupper(ans) == "Y"
                let cmd = printf('%s "%s" "%s" -t "%s" -o "%s" -f', s:python_path, s:h2cppx_path, a:header_file, s:template_file, cpp_file)
                let content = system(cmd)
                continue
            endif
        elseif v:shell_error == 5
            echohl WarningMsg | echo "IO error\n" . content | echohl None
        endif
        break
    endwhile
endfunction

function s:h2cppx_line(header_file, line_number, isClipboard)
    let ln = a:line_number
    let filename = expand('%:r') . "." . s:postfix
    let cpp_file = findfile(filename, join(s:search_list,","))

    let cmd = printf('%s "%s" "%s" -t "%s" -ln %d -a', s:python_path, s:h2cppx_path, a:header_file, s:template_file, ln)
    if ! (a:isClipboard == 1)
        if cpp_file == ""
            let dir = input("Cpp File not find, please enter the new file output directory: ")
            let cpp_file = s:fullpath(dir) . filename
        endif
        let cmd = cmd . " -o " . cpp_file
    endif
    let content = system(cmd)

    while 1
        if v:shell_error == 0
            if a:isClipboard == 1
                call setreg('"+', content . "\n")
                echo "Define code already copy to your clipboard,use p to paster!"
            else
                echo "write file " . cpp_file . " successful!"
            endif
        elseif v:shell_error == 1
            echo content
        elseif v:shell_error == 2
            echohl WarningMsg | echo content | echohl None
        elseif v:shell_error == 3
            echohl WarningMsg | echo content | echohl None
        elseif v:shell_error == 4
            "let ans = input("file already exisit, append to file tail?(yes/no): ")
            "if toupper(ans) == "YES" || toupper(ans) == "Y"
            "    let cmd = printf('%s "%s" "%s" -ln %d -a', s:python_path, s:h2cppx_path, a:header_file, ln)
            "    let content = system(cmd)
            "    continue
            "endif
        elseif v:shell_error == 5
            echohl WarningMsg | echo "IO error\n" . content | echohl None
        endif
        break
    endwhile
endfunction

function s:h2cppx_auto(header_file)
    let search_path = ""
    let filename = expand('%:r') . "." . s:postfix
    let cpp_file = findfile(filename, join(s:search_list,","))

    let cmd = printf('%s "%s" -t "%s" "%s" -auto -p %s ', s:python_path, s:h2cppx_path, s:template_file, a:header_file, s:postfix)
    if len(s:search_list) != 0
        let cmd = cmd . "--search-path=" . join(s:search_list,',')
    endif

    if cpp_file == ""
        let dir = input("Cpp File not find, please enter the new file output directory: ")
        let cmd = cmd . " --output-path=" . s:fullpath(dir)
    endif
    let content = system(cmd)

    while 1
        if v:shell_error == 0
            "let filename = expand('%:r') . "." . s:postfix
            "echo "Append code to " . filename . " successful!"
            echo content
        elseif v:shell_error == 1
            echo content
        elseif v:shell_error == 2
            echo content 
        elseif v:shell_error == 3
            echo content 
        elseif v:shell_error == 4
            echohl WarningMsg | echo "unknow error" | echohl None
        elseif v:shell_error == 5
            echohl WarningMsg | echo "IO error\n" . content | echohl None
        endif
        break
    endwhile
endfunction

function H2cppxLine(isClipboard)
    call s:h2cppx_line(expand('%:p'), line('.'), a:isClipboard)
endfunction

function H2cppx(isClipboard)
    call s:h2cppx(expand('%:p'), a:isClipboard)
endfunction

function H2cppxAuto()
    call s:h2cppx_auto(expand('%:p'))
endfunction


"generate cpp define and put in cpp file
command! -buffer -nargs=0 H2cppx call H2cppx(0)
command! -buffer -nargs=0 H2cppxLine call H2cppxLine(0)
"generate cpp define and put in clipboard
command! -buffer -nargs=0 CpH2cppx call H2cppx(1)
command! -buffer -nargs=0 CpH2cppxLine call H2cppxLine(1)
"auto generate cpp define 
command! -buffer -nargs=0 H2cppxAuto call H2cppxAuto()

