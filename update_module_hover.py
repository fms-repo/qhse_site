from pathlib import Path
import re
root = Path(r'd:\Other\Dev\qhse_site')
files = [
    'action-tracker.html',
    'audit.html',
    'emergency-drill.html',
    'fleet-management.html',
    'fit-to-work.html',
    'incident-management.html',
    'inspection.html',
    'journey-management.html',
    'management-of-change.html',
    'meeting.html',
    'risk-identification-loss-reporting.html',
    'training.html'
]
text_map = {
    'action-tracker-1.png': 'Centralized action tracking dashboard',
    'action-tracker-2.png': 'Action tracking interface for assignments',
    'action-tracker-3.png': 'Kanban board for action progress',
    'audit-1.png': 'Audit management dashboard',
    'audit-2.png': 'Audit report and findings interface',
    'emergency-drill-1.png': 'Emergency drill planning overview',
    'emergency-drill-2.png': 'Detailed drill execution interface',
    'fleet-1.png': 'Fleet tracking dashboard',
    'fleet-2.png': 'Vehicle operations interface',
    'fleet-3.png': 'Fleet Violations',
    'fleet-4.png': 'Violation Reports',
    'fit-to-work-1.png': 'Fit to work clearance dashboard',
    'incident-1.png': 'Incident Report',
    'incident-2.png': 'Incident reporting interface',
    'incident-3.png': 'Investigation detail view',
    'incident-4.png': 'Incident Quality Matrix',
    'inspection-1.png': 'Inspection dashboard overview',
    'inspection-2.png': 'Digital inspection checklist',
    'journey-1.png': 'Journey vehicle tracking',
    'journey-2.png': 'Journey logging Interface',
    'journey-3.png': 'Vehicle details',
    'journey-4.png': 'Journey management Vehicle compliance',
    'moc.jpeg': 'Management of change tracking',
    'meeting-1.png': 'Meeting scheduling dashboard',
    'meeting-2.png': 'Meeting Management ',
    'meeting-3.png': 'Meeting Detail',
    'rir-1.png': 'Risk identification dashboard',
    'rir-2.png': 'RIR Report',
    'rir-3.png': 'RIR Action Detail',
    'training-1.png': 'Training dashboard overview',
    'training-2.png': 'Training Bookings',
    'training-3.png': 'Training Matrix',
    'training-4.png': 'Certification tracking'
}

def wrap_slide(match):
    anchor = match.group(1)
    img = match.group(2)
    src = match.group(3)
    key = Path(src).name
    hover = text_map.get(key)
    if hover is None or 'slide-image-wrap' in anchor:
        return match.group(0)
    return f'{anchor}<div class="slide-image-wrap">{img}<div class="slide-hover-text">{hover}</div></div></a>'

for fname in files:
    path = root / fname
    content = path.read_text(encoding='utf-8')
    orig = content
    content = re.sub(
        r'(<a[^>]*class="[^"]*glightbox[^"]*"[^>]*>)(\s*<img[^>]+src="([^"]+)"[^>]*>\s*)(</a>)',
        wrap_slide,
        content,
        flags=re.DOTALL
    )

    def add_title(match):
        tag = match.group(0)
        src = match.group(1)
        if 'title=' in tag:
            return tag
        text = text_map.get(Path(src).name)
        if not text:
            return tag
        return tag[:-1] + f' title="{text}">'

    content = re.sub(r'<img[^>]+src="assets/img/([^"/]+)"[^>]*>', add_title, content)

    if '"pagination"' not in content:
        content = re.sub(
            r'(<script type="application/json" class="swiper-config">\s*\{)([^}]*?)(\}\s*</script>)',
            lambda m: m.group(1) + m.group(2) + '\n                              "pagination": {\n                                "el": ".swiper-pagination",\n                                "clickable": true\n                              },' + m.group(3),
            content,
            count=1,
            flags=re.DOTALL
        )

    if 'class="swiper-pagination"' not in content:
        content = re.sub(
            r'(</div>\s*</div>\s*</div>\s*</div>\s*</div>)(\s*<div class="tab-pane fade"|\s*<div class="tab-pane fade" id="service-details-tab-2")',
            lambda m: m.group(1) + '\n                          <div class="swiper-pagination"></div>' + m.group(2),
            content,
            count=1,
            flags=re.DOTALL
        )

    if content != orig:
        path.write_text(content, encoding='utf-8')
        print(f'Updated {fname}')
