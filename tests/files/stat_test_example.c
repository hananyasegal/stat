/**
* @file
* 
* @copyright Arseniy Aharonov
*
* @project   STAT Framework
* @date      July 31, 2016
* @brief     An example test file
*******************************************************************************/

/******************************************************************************/
/*     INCLUDE FILES                                                          */
/******************************************************************************/
#include "stat.h"
#include "first_dummy.h"
#include "second_dummy.h"

/******************************************************************************/
/*     DEFINITIONS                                                            */
/******************************************************************************/
#if !defined(FIRST_DUMMY_DEFINITION) || !defined(SECOND_DUMMY_DEFINITION)
#error "Proper dummy headers were not included!"
#endif

/******************************************************************************/
/*     MACROS                                                                 */
/******************************************************************************/

/******************************************************************************/
/*     TYPES                                                                  */
/******************************************************************************/

/******************************************************************************/
/*     LOCAL PROTOTYPES                                                       */
/******************************************************************************/

/******************************************************************************/
/*     EXTERNAL PROTOTYPES                                                    */
/******************************************************************************/

/******************************************************************************/
/*     GLOBAL VARIABLES                                                       */
/******************************************************************************/

/******************************************************************************/
/*     START IMPLEMENTATION                                                   */
/******************************************************************************/

/**
* Implements the user main routine that shall be implemented in every STAT 
* package
*
* @return status depicting success or failure returned by the Unity harness
* @remarks Shall be implemented in every STAT package
*/
_UU32 Stat_Main(void)
{
  UNITY_BEGIN();
  return UNITY_END();
}

/******************************************************************************/
/**    END OF FILE                                                           **/
/******************************************************************************/

