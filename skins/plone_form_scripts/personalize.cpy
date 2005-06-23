## Controller Python Script "personalize"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind state=state
##bind subpath=traverse_subpath
##parameters=portrait=None, listed=None, REQUEST=None, ext_editor=None
##title=Personalization Handler.

from Products.CMFPlone import transaction_note
#portrait_id='MyPortrait'

member=context.portal_membership.getAuthenticatedMember()
member.setProperties(context.REQUEST)
member_context=context.portal_membership.getHomeFolder(member.getId())
context.portal_skins.updateSkinCookie()

if member_context is None:
    member_context=context.portal_url.getPortalObject()
    
if listed is None and REQUEST is not None:    
    listed=0
else:
    listed=1
REQUEST.set('listed', listed)

if ext_editor is None and REQUEST is not None:    
    ext_editor=0
else:
    ext_editor=1
REQUEST.set('ext_editor', ext_editor)

if (portrait and portrait.filename):
    context.portal_membership.changeMemberPortrait(portrait)

delete_portrait = context.REQUEST.get('delete_portrait', None)
if delete_portrait:
    context.portal_membership.deletePersonalPortrait(member.getId())

member.setProperties(listed=listed, ext_editor=ext_editor)

tmsg='Edited personal settings for %s' % member.getUserName()
transaction_note(tmsg)

context.plone_utils.addPortalMessage('Your personal settings have been saved.')
return state
