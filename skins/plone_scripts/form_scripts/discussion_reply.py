## Script (Python) "discussion_reply"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=title,text,Creator
##title=Reply to content

replyID = context.createReply( title = title
                             , text = text
                             , Creator = Creator
                             )

target = '%s/%s' % (context.aq_parent.absolute_url(), context.aq_parent.getTypeInfo().getActionById('view'))

context.REQUEST.RESPONSE.redirect(target)

