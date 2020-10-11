type item = {
number: int;
name: string;
}
type contact = {
name: string*string; (*first and last name*)
phone: phone;
}
let get_name x = x.name
let myphone = {number=122; name="iphone";}
let _ = print_endline (get_name myphone)
