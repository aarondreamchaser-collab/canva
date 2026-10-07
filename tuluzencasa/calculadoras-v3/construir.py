"""Monta los JS finales de las calculadoras v3: inserta los aparatos de calculadora.js y minimiza con esbuild."""
import pathlib,subprocess
A=pathlib.Path(__file__).resolve().parent
ap=(A/'_aparatos.js').read_text()
app_=(A/'_aparatos_pot.js').read_text()
for n in ('consumo3','potencia3'):
    src=A/f'{n}.src.js'
    if not src.exists(): continue
    s=src.read_text().replace('/*APARATOS*/',ap).replace('/*APARATOS_P*/',app_)
    (A/f'{n}.js').write_text(s)
    r=subprocess.run(['npx','--yes','esbuild',str(A/f'{n}.js'),'--minify','--target=es2017','--legal-comments=none'],capture_output=True,text=True)
    if r.returncode: print(r.stderr); raise SystemExit(1)
    cab=s[:s.index('*/')+2]+'\n'
    (A/f'{n}.min.js').write_text(cab+r.stdout)
    print(n,len(s),'->',len(cab+r.stdout))
