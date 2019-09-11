(function() {
    $(document).ready(function() {
    var method_blocks = $('.method_block');
    $('select', method_blocks).on('change', switch_language);
    $('a[data-target]', method_blocks).on('click', switch_file)
    $('select', method_blocks).trigger('change');
})})();

function switch_language() {
    var el = $(this)
    var block = el.parent().parent();
    var value = el.val();

    $('.code_sample', block).addClass('hidden');
    $('.code_sample.code_sample_lang_' + value, block).removeClass('hidden');
    $('.code_sample.code_sample_lang_' + value + ' .code_import', block).addClass('hidden');
    $('.code_sample.code_sample_lang_' + value + ' .code_import', block).first().removeClass('hidden');
    $('a[data-target]:first-child', block).trigger('click');

};

function switch_file(e) {
    if(e != undefined) {
        e.stopPropagation();
        e.preventDefault();
    }    
    var el = $(this);
    var block = el.parent().parent();
    var target = el.data('target');
    $('.code_import', block).addClass('hidden');
    $('.code_import[data-filename="'+target+'"]', block).removeClass('hidden');
    $('a[data-target]', block).removeClass('disabled');
    el.addClass('disabled');
}