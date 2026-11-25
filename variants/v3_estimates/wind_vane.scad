// =====================================================================
//  Replacement wind-direction vane for VEVOR YT60231 weather station  (v3)
//  Two printed parts:
//    CAP   - bell-shaped hub. It slides onto the 2.8 mm D-shaft, locks with an
//            M2 set screw on the flat, and covers the bearing boss and the
//            tab with a skirt and drip lip (weather cap, like the original).
//            Printed UPSIDE DOWN (cap top on the bed), no supports.
//    BLADE - arm + half-barb arrow + tail fin + ballast pod, the v2 profile.
//            Printed upright (arm on the bed, fin standing up), no supports.
//    Joint: the blade's centre pad drops into a keyed slot across the cap top
//           and is clamped by one M3 x 14 screw + M3 nut (nut pocket in the cap).
//
//  Installed coordinates: Z = shaft axis, z = 0 at the housing top surface.
//  +X = arrow (into the wind), -X = tail.
//  part = "assembly" | "cap_print" | "blade_print" | "section" | "housing"
// =====================================================================
part = "assembly";

/* [Housing - ESTIMATES from photos: replace with caliper numbers] */
housing_top_d   = 35;    // flat top of the sensor housing
boss_d          = 12;    // raised bearing boss OD
boss_h          = 3.5;   // boss height above housing top (bearing top assumed flush)
shaft_protrusion= 16;    // shaft length above the bearing top
tab_outer_r     = 10.5;  // outermost edge of the hollow tab/post, from the shaft axis
tab_d           = 4;     // tab OD (only used for the housing dummy)
tab_h           = 5.5;   // tab height above housing top
tab_angle       = 270;   // where the tab sits (dummy/renders only; the cap clears it at any angle)

/* [Shaft & bore] */
shaft_d         = 2.8;
flat_depth      = 0.5;   // across-flat = shaft_d - flat_depth (2.3 assumed). MEASURE!
bore_clearance  = 0.15;
hub_gap         = 0.5;   // gap between the cap's inner boss and the bearing top (set with a shim)
bore_extra      = 1.5;   // extra bore depth above the shaft tip (tolerates a longer shaft)
bore_chamfer    = 0.4;

/* [Cap] */
skirt_clear_r   = 1.5;   // radial clearance from tab outer edge to skirt inner wall
tab_clear_z     = 1.0;   // minimum clearance from the shoulder to the tab top corner
rim_gap         = 1.5;   // skirt rim height above the housing top
wall            = 1.4;   // skirt / shoulder / neck wall thickness
lip_w           = 1.2;   // drip lip: outward overhang
lip_t           = 1.0;   // drip lip: flat rim thickness (lip top is a 45-degree shed)
neck_d          = 14;    // upper hub (neck) OD
core_d          = 8;     // inner bore boss OD
roof_t          = 1.0;   // solid material between the bore tip and the slot floor

/* [Set screw] */
screw_size      = "M2";  // "M2" or "M2.5"
screw_angle     = 90;    // CCW from the arrow; the flat is centred under the screw
screw_below_tip = 4.5;   // screw axis distance below the shaft tip (flat is on the upper shaft)
access_d        = 2.6;   // access hole through the neck wall (M2 set screw passes through)

/* [Blade joint] */
slot_d          = 6;     // depth of the keyed slot across the cap top
slot_clear      = 0.2;   // slot width = arm_w + slot_clear
pad_h           = 8;     // blade centre pad height (sits slot_d deep, rest proud)
pad_l           = 14;    // pad length (= neck_d)
joint_bolt_d    = 3.3;   // M3 clearance
joint_nut_af    = 5.5;   // M3 nut
joint_nut_t     = 2.4;

/* [Blade arms] */
arm_w           = 3.0;
arm_h           = 5.0;
nose_len        = 72;
barb_len        = 18;
barb_h          = 7;

/* [Tail fin] */
tail_len_top    = 100;
tail_len_bot    = 77;
fin_top_chord   = 33;
fin_h           = 45;    // fin top above the arm bottom
fin_root_x      = 11;
fin_curve       = 1.3;
fin_t           = 1.4;
fin_round       = 2;

/* [Ballast] */
ballast         = "nuts"; // "nuts" | "none"
ballast_nut     = "M6";
ballast_count   = 2;
ballast_x       = 37.3;   // BALANCE TUNING PARAMETER (tune.py)
pod_wall        = 1.2;
pod_floor       = 1.0;
pocket_clear    = 0.3;

$fn = 64;
eps = 0.01;

// ------------------------- derived -----------------------------------
tap_d    = (screw_size == "M2.5") ? 2.05 : 1.6;
bore_r   = (shaft_d + bore_clearance) / 2;
flat_y   = (shaft_d - flat_depth) - shaft_d/2 + bore_clearance/2;

z_bear   = boss_h;                              // bearing top
z_hb     = z_bear + hub_gap;                    // bottom of the cap's inner boss
z_tip    = z_bear + shaft_protrusion;           // shaft tip
bore_depth = shaft_protrusion - hub_gap + bore_extra;
z_bt     = z_hb + bore_depth;                   // top of the cylindrical bore
z_slot   = z_bt + bore_r + roof_t;              // slot floor = blade arm bottom
z_top    = z_slot + slot_d;                     // cap top
screw_z  = z_tip - screw_below_tip;

skirt_ri = tab_outer_r + skirt_clear_r;
skirt_ro = skirt_ri + wall;
neck_ro  = neck_d / 2;
neck_ri  = neck_ro - wall;
core_r   = core_d / 2;
z_c      = max(tab_h + tab_clear_z * sqrt(2) - (skirt_ri - tab_outer_r), rim_gap + 2); // skirt inner wall top (true 45-deg clearance >= tab_clear_z)
function z_in(r)  = z_c + (skirt_ri - r);                 // 45-degree inner shoulder
function z_out(r) = z_c + (skirt_ri - r) + wall * sqrt(2); // parallel outer shoulder
z_ann    = z_slot - 1.5;                        // top of the annular lightening gap

function bn(i) = ballast_nut == "M4" ? [7,3.2][i] : ballast_nut == "M5" ? [8,4][i]
               : ballast_nut == "M8" ? [13,6.5][i] : [10,5][i];
b_R      = (bn(0) + pocket_clear) / sqrt(3);
pod_r    = b_R + pod_wall;
pocket_h = ballast_count * bn(1) + 0.4;
pod_h    = pod_floor + pocket_h;

echo(str("V3: z_hb=", z_hb, " z_tip=", z_tip, " bore_depth=", bore_depth, " z_slot=", z_slot,
         " z_top=", z_top, " screw_z=", screw_z, " z_c=", z_c, " skirt OD=", 2*skirt_ro,
         " lip OD=", 2*(skirt_ro+lip_w), " radial clr=", skirt_ri - tab_outer_r,
         " vertical clr over tab=", z_in(tab_outer_r) - tab_h));

// hole along +Y, teardrop tip toward +Z (tip_up) or -Z (for parts printed upside down)
module teardrop_y(d, len, tip_up = true) {
    mirror([0,0, tip_up ? 0 : 1])
    rotate([90,0,0]) translate([0,0,-len]) linear_extrude(len)
        union() { circle(d = d); rotate(45) square(d/2); }
}

// ============================== CAP ==================================
module cap_body() {
    rotate_extrude() polygon([
        [0, z_top], [neck_ro - 0.8, z_top], [neck_ro, z_top - 0.8],
        [neck_ro, z_out(neck_ro)],
        [skirt_ro, z_out(skirt_ro)],
        [skirt_ro, rim_gap + lip_t + lip_w],
        [skirt_ro + lip_w, rim_gap + lip_t],      // 45-degree shed on top of the drip lip
        [skirt_ro + lip_w, rim_gap],
        [skirt_ri, rim_gap],
        [skirt_ri, z_c],
        [neck_ri, z_in(neck_ri)],
        [neck_ri, z_ann],
        [core_r, z_ann],
        [core_r, z_hb],
        [0, z_hb]]);
}

module d_bore() {
    intersection() {
        translate([0,0,z_hb - 1]) cylinder(r = bore_r, h = bore_depth + 1);
        translate([-6, -6, z_hb - 2]) cube([12, 6 + flat_y, bore_depth + 10]);
    }
    intersection() {   // drill-point roof (prints as a cone either way up)
        translate([0,0,z_bt - eps]) cylinder(r1 = bore_r, r2 = 0, h = bore_r);
        translate([-6, -6, z_hb]) cube([12, 6 + flat_y, bore_depth + 10]);
    }
    translate([0,0,z_hb - eps]) cylinder(r1 = bore_r + bore_chamfer, r2 = bore_r, h = bore_chamfer);
}

module set_screw_holes() {
    // tap hole in the core, from just inside the flat outward
    translate([0, flat_y - 0.5, screw_z]) teardrop_y(tap_d, core_r + 1 - flat_y, false);
    // screwdriver / screw access through the neck wall, coaxial
    translate([0, core_r - 0.2, screw_z]) teardrop_y(access_d, neck_ro + 2, false);
}

module joint_cuts() {
    // keyed slot across the cap top (along X, the vane axis)
    translate([-neck_ro - 1, -(arm_w + slot_clear)/2, z_slot]) cube([neck_d + 2, arm_w + slot_clear, slot_d + 1]);
    // M3 bolt across the slot (along Y), nut pocket on the -Y cheek
    zb = z_slot + slot_d/2;
    translate([0, -neck_ro - 1, zb]) teardrop_y(joint_bolt_d, neck_d + 2, false);
    translate([0, -neck_ro + 2.6, zb]) rotate([90,0,0])
        rotate(30) cylinder(r = (joint_nut_af + 0.3)/sqrt(3), h = 5, $fn = 6);
    // spot face for the screw head on the +Y cheek
    translate([0, neck_ro - 0.8, zb]) rotate([-90,0,0]) cylinder(d = 6.5, h = 5);
}

module cap() {
    difference() {
        cap_body();
        rotate(screw_angle - 90) { d_bore(); set_screw_holes(); }
        joint_cuts();
    }
}

// ============================= BLADE =================================
// blade-local coordinates: arm bottom at z = 0 (= z_slot when installed)
module plate_xz(t) { translate([0, t/2, 0]) rotate([90,0,0]) linear_extrude(t) children(); }

module fin_2d() {
    n = 24;
    lead = [for (i = [0:n]) let(u = i/n)
              [-(tail_len_top - fin_top_chord) + ((tail_len_top - fin_top_chord) - fin_root_x) * u,
               arm_h + (fin_h - arm_h) * pow(1-u, fin_curve)]];
    offset(r = fin_round) offset(delta = -fin_round)
        polygon(concat([[-tail_len_top, fin_h]], lead,
                       [[-fin_root_x, arm_h - 1], [-tail_len_bot, arm_h - 1]]));
}
module barb_2d() {
    x0 = nose_len - barb_len;
    polygon([[x0, 0], [nose_len, 0], [nose_len, 0.8], [x0 + 1.0, arm_h + barb_h], [x0, arm_h + barb_h]]);
}
module blade() {
    difference() {
        union() {
            translate([-tail_len_bot, -arm_w/2, 0]) cube([tail_len_bot + nose_len - barb_len + 1, arm_w, arm_h]);
            plate_xz(arm_w) barb_2d();
            plate_xz(fin_t) fin_2d();
            plate_xz(arm_w) polygon([[-tail_len_bot, arm_h - 0.5], [-fin_root_x, arm_h - 0.5],
                                     [-fin_root_x - 6, arm_h + 1.5], [-tail_len_bot + 2, arm_h + 1.5]]);
            // centre pad that keys into the cap slot (chamfered top corners)
            plate_xz(arm_w) polygon([[-pad_l/2, 0], [pad_l/2, 0], [pad_l/2, pad_h - 1.5],
                                     [pad_l/2 - 1.5, pad_h], [-pad_l/2 + 1.5, pad_h], [-pad_l/2, pad_h - 1.5]]);
            if (ballast == "nuts") translate([ballast_x, 0, 0]) cylinder(r = pod_r, h = pod_h, $fn = 48);
        }
        translate([0, -5, slot_d/2]) teardrop_y(joint_bolt_d, 10, true);
        if (ballast == "nuts")
            translate([ballast_x, 0, pod_floor]) rotate(30) cylinder(r = b_R, h = pocket_h + 1, $fn = 6);
    }
}

// ===================== stationary housing dummy ======================
module housing() {
    color("white") translate([0,0,-6]) cylinder(d = housing_top_d, h = 6);
    color("lightgray") difference() {
        cylinder(d = boss_d, h = boss_h);
        translate([0,0,-1]) cylinder(d = 7, h = boss_h + 2);
    }
    color("silver") difference() {           // flanged bearing (assumed 3x7 mm)
        cylinder(d = 7, h = boss_h);
        translate([0,0,-1]) cylinder(d = 3, h = boss_h + 2);
    }
    // tab/post with hole, joined to the boss by a thin web (placed at 200 deg)
    color("lightgray") rotate(tab_angle) {
        translate([tab_outer_r - tab_d/2, 0, 0]) difference() {
            cylinder(d = tab_d, h = tab_h);
            translate([0,0,1]) cylinder(d = tab_d - 2, h = tab_h);
        }
        translate([boss_d/2 - 0.5, -0.6, 0]) cube([tab_outer_r - tab_d/2 - boss_d/2 + 0.5, 1.2, tab_h - 1]);
    }
    color("gray") rotate(screw_angle - 90) intersection() {   // D-shaft
        translate([0,0,-4]) cylinder(d = shaft_d, h = z_tip + 4);
        translate([-5,-5,-4]) cube([10, 5 + shaft_d/2 - flat_depth, z_tip + 5]);
    }
}

module assembly() {
    color("teal") cap();
    color("darkcyan") translate([0,0,z_slot]) blade();
}

if (part == "assembly") assembly();
if (part == "cap") cap();
if (part == "blade") translate([0,0,z_slot]) blade();
if (part == "cap_print") translate([0,0,z_top]) rotate([180,0,0]) cap();
if (part == "blade_print") blade();
if (part == "housing") housing();
// swept envelope of everything stationary near the cap (tab swept 360 deg), for clearance checks
module stationary_envelope() {
    rotate_extrude() polygon([[0,-1],[boss_d/2,-1],[boss_d/2,0],[tab_outer_r,0],[tab_outer_r,tab_h],
                              [boss_d/2,tab_h],[boss_d/2,boss_h],[0,boss_h]]);
    translate([0,0,-6]) cylinder(d = housing_top_d, h = 6);
}
if (part == "envelope") stationary_envelope();
if (part == "section") {      // cut on the YZ plane (x = 0): shows set screw (+Y) and tab (-Y)
    difference() { union() { assembly(); housing(); } translate([0, -100, -20]) cube([200, 200, 200]); }
}
