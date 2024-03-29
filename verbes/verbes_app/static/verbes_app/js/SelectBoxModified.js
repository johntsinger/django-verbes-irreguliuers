'use strict';
{
    const SelectBox = {
        cache: {},
        init: function(id) {
            const box = document.getElementById(id);
            SelectBox.cache[id] = [];
            const cache = SelectBox.cache[id];
            // ADDED
            let verbes = JSON.parse(verbes_json);
            // Sort verbes by 'verbe' field necessary not to have an index shift when assigning the success and unsuccess classes
            // if the UserVerbes objects inside UserProfile have been modified
            verbes.sort(function (a, b) {
                return a.fields.verbe - b.fields.verbe;
            });
            // END ADDED
            for (const node of box.options) {
                // ADDED
                let i = node.value - 1
                if (verbes[i].fields.success == true) {
                    node.className = 'success';
                }
                else if (verbes[i].fields.success == false && verbes[i].fields.done == true) {
                    node.className = 'unsuccess';
                }
                else {
                    node.className = 'not-done';
                }
                // END ADDED
                // ADD CLASSNAME
                cache.push({value: node.value, text: node.text, className: node.className, displayed: 1});
            }
        },
        redisplay: function(id) {
            // Repopulate HTML select box from cache
            const box = document.getElementById(id);
            const scroll_value_from_top = box.scrollTop;
            box.innerHTML = '';
            // ADDED
            SelectBox.sort(id);
            // END ADDED
            for (const node of SelectBox.cache[id]) {
                if (node.displayed) {
                    const new_option = new Option(node.text, node.value, false, false);
                    // Shows a tooltip when hovering over the option
                    new_option.title = node.text;
                    // ADDED
                    new_option.className = node.className
                    // END ADDED
                    box.appendChild(new_option);
                }
            }
            box.scrollTop = scroll_value_from_top;
        },
        filter: function(id, text) {
            // Redisplay the HTML select box, displaying only the choices containing ALL
            // the words in text. (It's an AND search.)
            const tokens = text.toLowerCase().split(/\s+/);
            for (const node of SelectBox.cache[id]) {
                node.displayed = 1;
                const node_text = node.text.toLowerCase();
                for (const token of tokens) {
                    if (!node_text.includes(token)) {
                        node.displayed = 0;
                        break; // Once the first token isn't found we're done
                    }
                }
            }
            SelectBox.redisplay(id);
        },
        delete_from_cache: function(id, value) {
            let delete_index = null;
            const cache = SelectBox.cache[id];
            for (const [i, node] of cache.entries()) {
                if (node.value === value) {
                    delete_index = i;
                    break;
                }
            }
            cache.splice(delete_index, 1);
        },
        add_to_cache: function(id, option) {
            // ADD CLASSNAME
            SelectBox.cache[id].push({value: option.value, text: option.text, className: option.className, displayed: 1});
        },
        cache_contains: function(id, value) {
            // Check if an item is contained in the cache
            for (const node of SelectBox.cache[id]) {
                if (node.value === value) {
                    return true;
                }
            }
            return false;
        },
        move: function(from, to) {
            const from_box = document.getElementById(from);
            for (const option of from_box.options) {
                const option_value = option.value;
                if (option.selected && SelectBox.cache_contains(from, option_value)) {
                    // ADD CLASSNAME
                    SelectBox.add_to_cache(to, {value: option_value, text: option.text, className: option.className, displayed: 1});
                    SelectBox.delete_from_cache(from, option_value);
                }
            }
            SelectBox.redisplay(from);
            SelectBox.redisplay(to);
        },
        move_all: function(from, to) {
            const from_box = document.getElementById(from);
            for (const option of from_box.options) {
                const option_value = option.value;
                if (SelectBox.cache_contains(from, option_value)) {
                    // ADD CLASSNAME
                    SelectBox.add_to_cache(to, {value: option_value, text: option.text, className: option.className, displayed: 1});
                    SelectBox.delete_from_cache(from, option_value);
                }
            }
            SelectBox.redisplay(from);
            SelectBox.redisplay(to);
        }, // ADDED
        move_all_false: function(from, to) {
            const from_box = document.getElementById(from);
            for (const option of from_box.options) {
                const option_value = option.value;
                if (option.className == 'unsuccess' && SelectBox.cache_contains(from, option_value)) {
                    SelectBox.add_to_cache(to, {value: option_value, text: option.text, className: option.className, displayed: 1});
                    SelectBox.delete_from_cache(from, option_value);
                }
            }
            SelectBox.redisplay(from);
            SelectBox.redisplay(to);
        },
        move_all_not_done: function(from, to) {
            const from_box = document.getElementById(from);
            for (const option of from_box.options) {
                const option_value = option.value;
                if (option.className == 'not-done' && SelectBox.cache_contains(from, option_value)) {
                    SelectBox.add_to_cache(to, {value: option_value, text: option.text, className: option.className, displayed: 1});
                    SelectBox.delete_from_cache(from, option_value);
                }
            }
            SelectBox.redisplay(from);
            SelectBox.redisplay(to);
        }, // END ADDED
        sort: function(id) {
            SelectBox.cache[id].sort(function(a, b) {
                a = a.text.toLowerCase();
                b = b.text.toLowerCase();
                if (a > b) {
                    return 1;
                }
                if (a < b) {
                    return -1;
                }
                return 0;
            } );
        },
        select_all: function(id) {
            const box = document.getElementById(id);
            for (const option of box.options) {
                option.selected = true;
            }
        }
    };
    window.SelectBox = SelectBox;
}
