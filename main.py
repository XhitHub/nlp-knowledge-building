import app_repl as app
import _tests.t1 as t1
import _tests.t2 as appTest
import projects.all_the_news.control as atnControl

# testings
# app.run()
# t1.run()


# real deal
# atnControl.dataSourceToNLP()
# atnControl.dataSourceUnevenHeaderToNLP()
atnControl.dataSourceUnevenHeaderToNLP_v2(100)
# atnControl.classifyNLP('posSeq_d4')